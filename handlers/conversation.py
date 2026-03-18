import io
import logging

from fpdf import FPDF
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import config
from services import document, llm, memory

logger = logging.getLogger(__name__)

# Conversation states
AWAITING_CV, AWAITING_COMPANY, INTERVIEWING, FINAL_QUESTION, BEAST_MODE = range(5)

GREETING = (
    "Salut ! Je vais te faire passer un entretien d'embauche et te faire "
    "un retour détaillé à la fin.\n\n"
    "Pour commencer, envoie-moi ton CV, soit en texte directement ici, "
    "soit en pièce jointe (PDF ou DOCX)."
)

FINAL_QUESTION_TEXT = (
    "Avez-vous une remarque ou une question avant de finir cet entretien ?"
)


def _get_ids(update: Update) -> tuple[int, int]:
    return update.effective_user.id, update.effective_chat.id


def _build_qa_pairs(session: dict) -> list[tuple[str, str]]:
    qs = session["interview"]["questions"]
    ans = session["interview"]["answers"]
    return list(zip(qs, ans))


def _generate_report_pdf(report_text: str) -> bytes:
    """Generate a PDF from the report text and return raw bytes."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_font("Arial", "", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
    pdf.add_font("Arial", "B", "/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    pdf.set_font("Arial", "B", size=18)
    pdf.cell(0, 12, "Bilan d'entretien", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(8)
    pdf.set_font("Arial", "", size=11)
    for line in report_text.split("\n"):
        pdf.multi_cell(0, 6, line)
        pdf.ln(1)
    return pdf.output()


# ── /start ──────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id, chat_id = _get_ids(update)
    memory.reset_session(user_id, chat_id)
    context.user_data.clear()
    await update.message.reply_text(GREETING)
    return AWAITING_CV


# ── CV handlers ─────────────────────────────────────────────────────────────

async def handle_cv_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    raw_text = update.message.text
    user_id, chat_id = _get_ids(update)
    if await llm.check_offensive(raw_text):
        session = memory.load_session(user_id, chat_id)
        return await _enter_beast_mode(update, context, session, raw_text)
    return await _process_cv(update, context, raw_text)


async def handle_cv_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    doc = update.message.document
    file_name = (doc.file_name or "").lower()

    if not file_name.endswith((".pdf", ".docx")):
        await update.message.reply_text(
            "Je ne peux pas lire ce format, envoie-moi un PDF ou un DOCX."
        )
        return AWAITING_CV

    await update.message.reply_text("Je lis ton document, deux secondes...")

    file = await context.bot.get_file(doc)
    buffer = io.BytesIO()
    await file.download_to_memory(buffer)
    file_bytes = buffer.getvalue()

    if file_name.endswith(".pdf"):
        raw_text = document.extract_text_from_pdf(file_bytes)
    else:
        raw_text = document.extract_text_from_docx(file_bytes)

    if not raw_text.strip():
        await update.message.reply_text(
            "Je n'arrive pas à lire le contenu de ce fichier. "
            "Tu peux m'envoyer ton CV en texte directement ?"
        )
        return AWAITING_CV

    return await _process_cv(update, context, raw_text)


async def _process_cv(update: Update, context: ContextTypes.DEFAULT_TYPE, raw_text: str) -> int:
    user_id, chat_id = _get_ids(update)

    result = await llm.evaluate_cv(raw_text)

    if not result["satisfactory"]:
        await update.message.reply_text(
            f"{result['feedback']} Renvoie-moi ton CV avec un peu plus de détails."
        )
        return AWAITING_CV

    # Save CV to memory
    session = memory.load_session(user_id, chat_id)
    session["cv"] = result["reformatted_cv"]
    memory.save_session(user_id, chat_id, session)

    await update.message.reply_text(
        f"{result['feedback']} "
        "Maintenant dis-moi pour quel poste et quelle entreprise tu postules. "
        "Tu peux me coller l'offre d'emploi ou juste me décrire le truc."
    )
    return AWAITING_COMPANY


# ── Company handler ─────────────────────────────────────────────────────────

async def handle_company(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    raw_text = update.message.text
    user_id, chat_id = _get_ids(update)
    if await llm.check_offensive(raw_text):
        session = memory.load_session(user_id, chat_id)
        return await _enter_beast_mode(update, context, session, raw_text)

    result = await llm.evaluate_company(raw_text)

    if not result["satisfactory"]:
        await update.message.reply_text(
            f"{result['feedback']} Donne-moi un peu plus de détails sur le poste et l'entreprise."
        )
        return AWAITING_COMPANY

    # Save company to memory
    session = memory.load_session(user_id, chat_id)
    session["company"] = result["description"]
    memory.save_session(user_id, chat_id, session)

    # Generate first question
    question = await llm.generate_question(session["cv"], session["company"], [])
    session["interview"]["questions"].append(question)
    memory.save_session(user_id, chat_id, session)
    context.user_data["question_index"] = 0

    msg = await update.message.reply_text(
        f"C'est bon, on commence l'entretien. "
        f"Je vais te poser {config.NUMBER_OF_INTERVIEW_QUESTIONS} questions, "
        f"réponds comme tu le ferais face à un vrai recruteur.\n\n{question}"
    )
    context.user_data["question_message_id"] = msg.message_id
    return INTERVIEWING


# ── Interview Q&A handler ──────────────────────────────────────────────────

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Ignore stale messages sent before the question (e.g. split long messages)
    q_msg_id = context.user_data.get("question_message_id", 0)
    if update.message.message_id < q_msg_id:
        return INTERVIEWING

    answer_text = update.message.text
    user_id, chat_id = _get_ids(update)
    session = memory.load_session(user_id, chat_id)
    q_index = context.user_data.get("question_index", 0)
    current_question = session["interview"]["questions"][q_index]

    # Evaluate the answer
    eval_result = await llm.evaluate_answer(
        current_question, answer_text, session["cv"], session["company"]
    )

    if eval_result["status"] == "offensive":
        return await _enter_beast_mode(update, context, session, answer_text)

    if eval_result["status"] == "unsatisfactory":
        await update.message.reply_text(
            f"{eval_result['feedback']}\n\n{current_question}"
        )
        return INTERVIEWING

    # Store the accepted answer
    session["interview"]["answers"].append(answer_text)
    memory.save_session(user_id, chat_id, session)

    answered_count = len(session["interview"]["answers"])
    total = config.NUMBER_OF_INTERVIEW_QUESTIONS

    # Check if we've answered N-1 questions → ask the final fixed question
    if answered_count == total - 1:
        session["interview"]["questions"].append(FINAL_QUESTION_TEXT)
        memory.save_session(user_id, chat_id, session)
        context.user_data["question_index"] = answered_count

        msg = await update.message.reply_text(
            f"{eval_result['feedback']}\n\n{FINAL_QUESTION_TEXT}"
        )
        context.user_data["question_message_id"] = msg.message_id
        return FINAL_QUESTION

    # Generate next question
    qa_pairs = _build_qa_pairs(session)
    next_question = await llm.generate_question(
        session["cv"], session["company"], qa_pairs
    )
    session["interview"]["questions"].append(next_question)
    memory.save_session(user_id, chat_id, session)
    context.user_data["question_index"] = answered_count

    msg = await update.message.reply_text(
        f"{eval_result['feedback']}\n\n{next_question}"
    )
    context.user_data["question_message_id"] = msg.message_id
    return INTERVIEWING


# ── Final question handler ──────────────────────────────────────────────────

async def handle_final_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Ignore stale messages sent before the question
    q_msg_id = context.user_data.get("question_message_id", 0)
    if update.message.message_id < q_msg_id:
        return FINAL_QUESTION

    answer_text = update.message.text
    user_id, chat_id = _get_ids(update)
    session = memory.load_session(user_id, chat_id)
    q_index = context.user_data.get("question_index", 0)
    current_question = session["interview"]["questions"][q_index]

    eval_result = await llm.evaluate_answer(
        current_question, answer_text, session["cv"], session["company"]
    )

    if eval_result["status"] == "offensive":
        return await _enter_beast_mode(update, context, session, answer_text)

    if eval_result["status"] == "unsatisfactory":
        await update.message.reply_text(
            f"{eval_result['feedback']}\n\n{current_question}"
        )
        return FINAL_QUESTION

    # Store the final answer
    session["interview"]["answers"].append(answer_text)
    memory.save_session(user_id, chat_id, session)

    # Generate the report
    await update.message.reply_text("C'est terminé ! Je te prépare ton bilan en PDF, ça peut prendre un moment...")

    qa_pairs = _build_qa_pairs(session)
    report = await llm.generate_report(session["cv"], session["company"], qa_pairs)

    pdf_bytes = _generate_report_pdf(report)
    pdf_file = io.BytesIO(pdf_bytes)
    pdf_file.name = "bilan_entretien.pdf"
    await update.message.reply_document(document=pdf_file, filename="bilan_entretien.pdf")
    return ConversationHandler.END


# ── Beast mode ──────────────────────────────────────────────────────────────

async def _enter_beast_mode(
    update: Update, context: ContextTypes.DEFAULT_TYPE, session: dict, trigger_message: str
) -> int:
    """Trigger the first beast-mode response and enter BEAST_MODE state."""
    context.user_data["beast_history"] = []
    cv = session.get("cv") or ""
    company = session.get("company") or ""
    response = await llm.generate_beast_response(
        trigger_message, cv, company, []
    )
    context.user_data["beast_history"].append((trigger_message, response))
    await update.message.reply_text(response)
    return BEAST_MODE


async def handle_beast_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_message = update.message.text
    user_id, chat_id = _get_ids(update)
    session = memory.load_session(user_id, chat_id)
    beast_history: list[tuple[str, str]] = context.user_data.get("beast_history", [])

    response = await llm.generate_beast_response(
        user_message, session["cv"], session["company"], beast_history
    )
    beast_history.append((user_message, response))
    context.user_data["beast_history"] = beast_history
    await update.message.reply_text(response)
    return BEAST_MODE


# ── Cancel ──────────────────────────────────────────────────────────────────

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Entretien annulé. Tu peux relancer avec /start quand tu veux.")
    return ConversationHandler.END


# ── Build the ConversationHandler ───────────────────────────────────────────

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        AWAITING_CV: [
            MessageHandler(filters.Document.ALL, handle_cv_document),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_cv_text),
        ],
        AWAITING_COMPANY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_company),
        ],
        INTERVIEWING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer),
        ],
        FINAL_QUESTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_final_answer),
        ],
        BEAST_MODE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_beast_mode),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True,
)
