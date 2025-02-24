# InsureRight - BisonHacks Hackathon 2025 First Place Winner

## Overview

This repository contains the source code for an AI-powered insurance application developed during BisonHacks 2025. The app leverages artificial intelligence to streamline the insurance process, offering users summarized insurance policies and benefits, efficient claims filing, and helping users to file insurance-related cases.

## Features

- **Summarized Insurance Policies and Benefits: Utilizes AI to provide users with concise summaries of complex insurance policies, making it easier to understand coverage details.
- **Efficient Claims Filing: Simplifies the claims process with an intuitive interface and AI assistance, reducing the time and effort required to file a claim.
- **Assistance with Insurance-Related Cases: Guides users through the process of filing insurance-related cases, ensuring all necessary steps are followed correctly.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/ahmed-shami/BisonHacks2025.git
   ```bash
   cd BisonHacks2025

2. **Install Dependencies: Ensure you have Python 3.x installed. Then, install the required Python packages:**
   ```bash
   pip install -r requirements.txt

3. **Set Up Environment Variables: Create a .env file in the root directory and add any necessary environment variables, such as API keys or database URLs. For example:**
   ```bash
   API_KEY=your_api_key_here
   ```bash
   DATABASE_URL=your_database_url_here

4. **Apply Database Migrations: If the project uses a database, apply the necessary migrations:**

   python manage.py migrate
5. **Run the Application: Start the development server:**
   ```bash
   python manage.py runserver
