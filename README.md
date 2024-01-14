# Asset Portfolio Tracker Application

This app help you track your asset portfolio. Everything from stocks, to crypto, .etc.

## Features

- Track your asset portfolio
- Get notified when the price of your asset changes
- Get monthly, weekly, daily report about your portfolio performance
- Get insights about your portfolio

## Todo

- [x] Add asset portfolio tracking API
- [x] Implement JWT authentication
- [ ] UI for asset portfolio tracking
- [ ] Admin dashboard
- [ ] Add authorization
- [ ] Caching for API
- [ ] Implement SSO with Google, Facebook, .etc
- [ ] Notify price changes
- [ ] Send monthly, weekly, daily report to user about their portfolio performance
- [ ] Using AI to give insights about user portfolio
- [ ] Use ML to recommend assets to user based on their portfolio, risk tolerance, investment goals, .etc
- [ ] News blog about finance, investment, .etc
- [ ] Add tests for API
- [ ] Add tests for UI
- [ ] Add CI/CD
- [ ] Logging
- [ ] Mobile app (React Native)

## Tech Stack

**Client:** Vite + React, TypeScript, TailwindCSS, Shadcn

**Server:** FastAPI, PostgreSQL

## Development

### Prerequisites

- Docker
- Python 3.9
- NodeJS 14.17.0

### Environment Variables

To run this project, you will need to add the following environment variables to your .env and .env.local file. Refer to .env.example for more details.

### Start the development server and client

To run this project, you will need clone this project and run the following commands

For Linux/MacOS:

```bash
  make dev
```

For Windows:

```bash
  docker-compose up -d
```

Then, open your browser and go to `http://localhost:80`

## Contributing

Contributions are always welcome!

## Authors

- [@Son Pham](https://github.com/RoadToDev101)
