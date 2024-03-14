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

This application support 2 types of templates in YAML format.

With command you can get list of calendars.

```bash
python main.py --ls-cal
```

First one is for all day events, like payments or taxes. With follow command you can generate events from you template to calendar.
Specify name, duration, date and color for your event. The `business_day` flag serves to indicate if the event should be during business day. If this flag is true, the event will be moved to closes date before the week end.

### { YOU_CALENDAR_ID }

It should be id from list of calendars.
`Calendar: Month plan, ID: {xxxxxxxxxxx}@group.calendar.google.com` - copy symbols before @ sign.

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

## Google Calendar API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Once in your project, go to the "Library" section and enable the "Google Calendar API".
4. Go to the "Credentials" section and create new credentials. Choose "OAuth client ID".
5. Configure the OAuth consent screen. Choose "External" for the user type. Fill in the necessary details.
6. When creating the OAuth client ID, select "Desktop app" as the application type.
7. Download the JSON file of your credentials.
8. Copy you calendar id to you .yml file as calendar-id.
9. Execute from command line script to get list of calendars.

```bash
python main.py --ls-cal
```

10. Run to push events from YAML template ro Google calendar.

```bash
python main.py --frame next-month --template month_plan.yaml
```

```bash
python main.py --frame next-week --template week_plan.yaml
```

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
