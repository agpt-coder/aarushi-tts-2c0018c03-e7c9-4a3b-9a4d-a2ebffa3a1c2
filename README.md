---
date: 2024-04-16T14:02:38.909101
author: AutoGPT <info@agpt.co>
---

# aarushi-tts-2

Based on the information gathered, the project involves creating a feature or API endpoint to convert input text into natural-sounding speech audio, primarily for educational materials. Key requirements and considerations include:

1. **Audio Output Format:** The output should be available in MP3 format, ensuring broad compatibility.

2. **Language and Accent Support:** The speech synthesis must support English with an American accent, aiming for broad accessibility and ease of understanding.

3. **Voice Characteristics:** A female voice is preferred due to its clear and soothing characteristics, suitable for most listening contexts.

4. **Customization Capabilities:** Users need the ability to control speech synthesis parameters, including speech speed, pitch, and volume. This customization facilitates tailored audio outputs that cater to diverse needs and preferences.

5. **Input Text Formats:** The system should accept both plain text and SSML (Speech Synthesis Markup Language) inputs. Plain text offers straightforward usability, while SSML provides nuanced control over the speech synthesis process, enabling richer and more expressive audio outputs.

6. **Best Practices for API Design:** Implementing this text-to-speech (TTS) feature as a REST API involves adhering to best practices such as supporting multiple audio formats, ensuring scalability, utilizing caching mechanisms, securing API access and data transmission, imposing rate limits, offering customization options, promoting accessibility and internationalization, providing comprehensive documentation, and setting up monitoring and feedback mechanisms.

**Tech Stack:** The recommended tech stack includes Python for programming, FastAPI for the API framework given its asynchronous capabilities and ease of use for creating RESTful APIs, PostgreSQL for the database due to its reliability and performance, and Prisma as the ORM to facilitate easy and secure database operations within a Python and FastAPI environment.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'aarushi-tts-2'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
