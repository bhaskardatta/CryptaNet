# CryptaNet Frontend

This is the frontend dashboard for the CryptaNet system, providing a user-friendly interface for visualizing supply chain data, anomaly alerts, and explanations.

## Features

- **Dashboard**: Overview of supply chain metrics and anomaly alerts
- **Data Visualization**: Interactive charts and graphs for supply chain data
- **Anomaly Detection**: Visual representation of detected anomalies
- **Explainability**: Human-readable explanations for detected anomalies
- **Data Management**: Interface for submitting and retrieving supply chain data
- **Access Control**: Role-based access control for different organizations

## Technology Stack

- **React.js**: Frontend framework
- **Redux**: State management
- **Material-UI**: UI component library
- **Chart.js**: Data visualization
- **Axios**: API client for backend communication

## Project Structure

```
frontend/
├── public/              # Public assets
│   ├── index.html      # HTML entry point
│   └── favicon.ico     # Favicon
├── src/                # Source code
│   ├── components/     # Reusable UI components
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── store/          # Redux store
│   ├── utils/          # Utility functions
│   ├── App.js          # Main application component
│   └── index.js        # JavaScript entry point
├── package.json        # Dependencies and scripts
└── README.md           # Documentation
```

## Installation and Setup

1. Install dependencies
   ```bash
   npm install
   ```

2. Start the development server
   ```bash
   npm start
   ```

3. Build for production
   ```bash
   npm run build
   ```

## Development Guidelines

- Follow the React component structure and naming conventions
- Use functional components with hooks instead of class components
- Implement responsive design for all components
- Write unit tests for components and services
- Document code with JSDoc comments

## API Integration

The frontend communicates with the backend API for the following operations:

- Authentication and authorization
- Submitting supply chain data
- Retrieving supply chain data
- Querying anomaly detection results
- Retrieving explanations for anomalies

## Security Considerations

- Implement proper authentication and authorization
- Secure API communication with HTTPS
- Validate user input
- Handle sensitive data securely
- Implement proper error handling