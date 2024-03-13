# Perfect Week Generator

## Description

This application provides routine automation to add template tasks to your Google calendar.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository (`git clone https://github.com/mi-heorhi/perfect-week-generator.git`)
2. Install dependencies.
3. Your template for a week events could be stored on github as a private repository.

## Google Calendar API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Once in your project, go to the "Library" section and enable the "Google Calendar API".
4. Go to the "Credentials" section and create new credentials. Choose "OAuth client ID".
5. Configure the OAuth consent screen. Choose "External" for the user type. Fill in the necessary details.
6. When creating the OAuth client ID, select "Desktop app" as the application type.
7. Download the JSON file of your credentials.

## Contributing

1. Fork the Project
2. Clone the repository (`git clone https://github.com/mi-heorhi/perfect-week-generator.git`)
3. Create a new branch (`git checkout -b feature/feature-name`)
4. Make your changes, make sure your not commit you private schedule to public repo or your credential json files.
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/feature-name`)
7. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
