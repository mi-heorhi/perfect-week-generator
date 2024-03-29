# Perfect Week Generator

## Description

This application provides routine automation to add template tasks to your Google calendar.

## Requirements

1. Python 3.9: The code snippets provided are in Python, so you'll need to have Python installed on your machine.
2. Pip: The Python package installer is used to install the project's dependencies.
3. Google Calendar API: The application interacts with Google Calendar, so you'll need access to the Google Calendar API.
4. YAML files: The application uses YAML files as templates for events.
5. Git: The usage instructions suggest that you'll need Git to clone the repository.
6. A Google account: Since this application interacts with Google Calendar, you'll need a Google account.
7. Dependencies listed in the requirements.txt file: You'll need to install these using pip.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository (`git clone https://github.com/mi-heorhi/perfect-week-generator.git`)
2. Install dependencies.
3. Your template for a week events could be stored on github as a private repository.

This application support 2 types of templates in YAML format.

With command you can get list of calendars.

```bash
python main.py --ls-cal
```

First one is for all day events, like payments or taxes. With follow command you can generate events from you template to calendar.
Specify name, duration, date and color for your event. The `business_day` flag serves to indicate if the event should be during business day. If this flag is true, the event will be moved to closes date before the week end.

```yaml
version: 1
type: all-day
calendar-id: { YOU_CALENDAR_ID }
entries:
  - name: Destroy the ring in fire of Mountain Doom
    description: Some description
    date: 1
    business_day: false
    color: "#FED5CF" # Should be HEX formate
```

Second for events that could happened during your productive day. Run this command to generate you perfect week template to you Google calendar.

```bash
python main.py --frame next-week --template week_plan.yaml
```

```yaml
version: 1
type: single
calendar-id: { YOU_CALENDAR_ID }
week:
  1: # Monday
    - name: Wake Up
      startAt: 10-00
      duration: 15
      color: "#BEDAE3"
      description: Good Morning
    - name: Morning planing
      startAt: 10-00
      duration: 15
      color: "#BEDAE3"
      description: Keep-up.
  2: # Tuesday
  3: # ...
  4: # ...
  5: # ...
  6: # ...
  7: # ...
```

### { YOU_CALENDAR_ID }

It should copied output of `python main.py --ls-cal` from list of calendars.
`Calendar: Month plan, ID: {xxxxxxxxxxx}@group.calendar.google.com` - copy symbols before @ sign. Past this id to you template, to define destination calendar.

```bash
python main.py --frame next-month --template month_plan.yaml
```

```bash
python main.py --frame next-week --template week_plan.yaml
```

## Google Calendar API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Once in your project, go to the "Library" section and enable the "Google Calendar API".
4. Go to the "Credentials" section and create new credentials. Choose "OAuth client ID".
5. Configure the OAuth consent screen. Choose "External" for the user type. Fill in the necessary details.
6. When creating the OAuth client ID, select "Desktop app" as the application type.
7. Download the JSON file of your credentials to directory with main.py file.

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
