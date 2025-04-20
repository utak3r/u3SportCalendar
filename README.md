# u3SportCalendar

For now it's just a GUI-less app, but after it's fully working I'll add some GUI for easy configuring.

Right now fully working is a *TransferMarkt* scraper. To get your endpoint, find your team and go to page **Fixtures -> Fixtures by date**.

See this example **config.json**:
```json
{
	"events_calendar": "YOUR_GOOGLE_CALENDAR_ID@group.calendar.google.com",
	"how_many_days": 60,
	"update_hour": true,
	"sources": [
		{
			"name": "Pogon",
			"api": "TransferMarkt",
			"endpoint": "pogon-stettin/spielplandatum/verein/324"
		},
		{
			"name": "Real",
			"api": "TransferMarkt",
			"endpoint": "real-madrid/spielplandatum/verein/418"
		},
		{
			"name": "Arsenal",
			"api": "TransferMarkt",
			"endpoint": "fc-arsenal/spielplandatum/verein/11"
		},
		{
			"name": "Barcelona",
			"api": "TransferMarkt",
			"endpoint": "fc-barcelona/spielplandatum/verein/131"
		}
	]
}
```

If you set `update_hour` to `true`, it will check if the event already exists with the same teams in the same day, but on a different hour - and replace it with a new event. If not, it will be strictly checking an hour.

For now, stay tuned for fixes and GUI :)
