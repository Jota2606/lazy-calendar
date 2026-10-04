Claro. Te lo dejaría así: técnico pero limpio, orientado a que alguien que vea el repositorio entienda rápidamente qué hace, cómo funciona y cómo ejecutarlo.

# Horario UNIC

Desktop application that converts a university timetable image into editable calendar events and Excel data.

The application uses OCR to recognize the structure and content of a timetable, processes the extracted information, allows the user to review and manually correct the detected events, and finally exports the timetable to iCalendar (`.ics`) and Excel (`.xlsx`).

It can also send the generated calendar directly by email using Gmail SMTP.

## Features

- Select a timetable image.
- Automatic timetable recognition using OCR.
- Detection of days, time slots, subjects, teachers, and locations.
- JSON intermediate representation between OCR and parsing.
- Automatic event parsing and normalization.
- Manual review of all detected events.
- Manual editing of any event before export.
- Event validation before export.
- iCalendar (`.ics`) export.
- Excel (`.xlsx`) export.
- `Africa/Luanda` timezone support.
- Automatic calendar delivery by email using Gmail SMTP.
- Desktop graphical interface built with Tkinter.

## How It Works

```text
Timetable Image
       ↓
      OCR
       ↓
   JSON Data
       ↓
    Parsers
       ↓
 Normalization
       ↓
 Review & Edit
       ↓
   Validation
       ↓
 ┌───────────────┐
 │               │
 ▼               ▼
iCalendar      Excel
 │
 ▼
Email
 │
 ▼
Calendar App
```

The JSON layer acts as the contract between the OCR system and the parsers. This makes the processing pipeline easier to debug, test, and develop independently.

## Project Structure

```text
Horario-Unic/
│
├── models/
│   └── horario.py
│
├── ocr/
│   └── ocr.py
│
├── parsers/
│   ├── parser.py
│   ├── entrada.py
│   ├── estructura.py
│   ├── celdas.py
│   └── eventos.py
│
├── normalizadores/
│   └── normalizador.py
│
├── validators/
│   └── validator.py
│
├── exportadores/
│   ├── ical.py
│   ├── excel.py
│   └── correo.py
│
├── dev/
│   └── Development and testing scripts
│
├── output/
│   └── Generated files
│
├── interfaz.py
├── interfaz_revision.py
├── interfaz_exportacion.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

- Python 3.12
- Windows
- Internet connection during dependency installation and the initial OCR model download.

## Installation

Clone the repository:

```bash
git clone <REPOSITORY_URL>
cd Horario-Unic
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Email Configuration

Email delivery is optional.

To enable automatic calendar delivery, create a `.env` file in the project root:

```text
SMTP_EMAIL=your@gmail.com
SMTP_PASSWORD=your_app_password
DESTINO_EMAIL=your@gmail.com
```

`SMTP_PASSWORD` must be a Google App Password, not the normal password of the Gmail account.

The `.env` file is included in `.gitignore` and **must never be committed to the repository**.

## Usage

Run the application:

```powershell
python main.py
```

The application workflow is:

1. Select the timetable image.
2. Wait for the OCR process to finish.
3. Review the detected events.
4. Manually correct any OCR errors if necessary.
5. Click **Export**.
6. Select the Monday corresponding to the timetable week.
7. Export the timetable.
8. Optionally send the generated calendar by email.

The generated `.ics` file can be imported into Apple Calendar and other applications supporting the iCalendar format.

## OCR Accuracy

OCR systems can make mistakes, especially when:

- The image contains reflections or glare.
- Text is small or difficult to read.
- Cells are merged.
- Text is partially obscured.
- The source image has low quality.

For this reason, Horario UNIC includes a manual review stage before export.

**Always review the detected events before exporting the timetable.**

The application intentionally does not assume that every OCR result is correct. Automatic normalization is only applied to corrections that can be determined with reasonable confidence, while uncertain results are left available for manual correction.

## Output Formats

### iCalendar

The application generates a `.ics` calendar containing the timetable events.

Events use the following timezone:

```text
Africa/Luanda
```

This ensures that timetable times are represented using Angola's local timezone.

### Excel

The application also generates an `.xlsx` file containing the extracted timetable information.

The spreadsheet currently includes:

- Day
- Start time
- End time
- Subject
- Teacher
- Location
- Event type

## Technologies

- **Python**
- **Tkinter** — Desktop graphical interface
- **PaddleOCR / PaddlePaddle** — OCR and timetable structure recognition
- **iCalendar** — Calendar file generation
- **OpenPyXL** — Excel generation
- **tkcalendar** — Calendar date selection
- **python-dotenv** — Environment variable management
- **Gmail SMTP** — Calendar email delivery

## Current Status

The application currently has a complete functional workflow:

- [x] Timetable image selection
- [x] OCR processing
- [x] JSON OCR output
- [x] Timetable structure parsing
- [x] Event generation
- [x] Event normalization
- [x] Manual event review
- [x] Manual event editing
- [x] Event validation
- [x] iCalendar export
- [x] Excel export
- [x] Angola timezone support
- [x] Email delivery of the generated calendar

Future improvements will primarily focus on quality-of-life features, user experience, OCR accuracy, application distribution, and packaging the project as a standalone Windows application.

## Disclaimer

Horario UNIC is an OCR-based automation tool. Its output should be considered a first interpretation of the timetable rather than guaranteed ground truth.

Always verify the generated events before adding them to your personal calendar.

## License

This project is currently intended for personal use.

Yo usaría **exactamente este README** por ahora. Está documentando el estado real de la aplicación sin vender funcionalidades que todavía no existen, y además deja preparado el terreno para cuando hagamos el `.Setup.exe`.