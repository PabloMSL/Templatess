from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import os
import django
import sys
sys.path.append(r"C:\Users\SENA\Desktop\django")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Hospital.settings")
django.setup()


# Tu token aquí
TOKEN = "8498321679:AAHDbkJVg1xEZXoTHyeqOyT15OAyYfgr7Ss"  # Cambia por tu token real

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    message = """
🏥 ¡Bienvenido al Hospital Moderno! 
    
Este bot te ayudará a:
✅ Ver tu historial medico
✅ Consultar tus citas
✅ Buscar medicamentos
✅ Consultar doctores y sus especialidades

Usa /help para más comandos.
    """
    await update.message.reply_text(message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help"""
    help_text = """
📚 Comandos disponibles:

/start - Inicia el bot
/help - Muestra esta ayuda
/historial - Ver mi historial medico
/citas - Ver mis citas programadas y canceladas
/med - Ver medicamentos de la receta
/doc - Consultar los doctores
    """
    await update.message.reply_text(help_text)

async def ver_historial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver historial del usuario"""
    from Paciente.models import HistorialMedico
    
    try:
        # Obtener ID del usuario de Telegram (si está vinculado)
        user_id = update.effective_user.id
        
        # Aquí irían las consultas a tu BD
        message = "📋 Tu historial:\n\n"
        message += "1. Cita de odontologia - 12/10/2025 04:00 PM\n"
        message += "2. Cita general - 20/7/2025 2:00 PM\n"
        message += "3. Cita de oftalmologia - 13/5/2025 08:00 AM\n"
        
        await update.message.reply_text(message)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

async def ver_citas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver citas pendientes"""
    message = "🕑 Citas pendientes:\n\n"
    message += "1. Cita de cardiologia - 12/01/2026\n"
    message += "2. Cita de optometria -  28/12/2025\n"
    message += "3. Cita general - 02/02/2026 \n"
    
    await update.message.reply_text(message)

async def ver_doctor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ver perfil del doctor"""
    message = """
👤 Perfil del Doctor:

Nombre: Johan Sebastian Castro Gonzalez
Email: johan@example.com
Rol: Optometrista
Habitacion : 101
    """
    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar mensajes generales"""
    user_message = update.message.text.lower()
    
    if "hola" in user_message:
        await update.message.reply_text("¡Hola! 👋 ¿En qué puedo ayudarte?")
    elif "ayuda" in user_message:
        await update.message.reply_text("Usa /help para ver todos los comandos disponibles.")
    else:
        await update.message.reply_text("No entendí. Usa /help para ver los comandos.")

def main():
    """Inicia el bot"""
    # Crear aplicación
    application = Application.builder().token(TOKEN).build()
    
    # Handlers de comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("historial", ver_historial))
    application.add_handler(CommandHandler("citas", ver_citas))
    application.add_handler(CommandHandler("doc", ver_doctor))
    
    # Handler para mensajes
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Inicia polling
    print("Bot iniciado... Esperando mensajes")
    application.run_polling()

if __name__ == '__main__':
    main()