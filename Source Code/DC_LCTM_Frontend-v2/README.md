# Deepcytes Live Cyber Threat Map (LCTM)

A modern React-based application that visualizes real-time cyber threats and attacks on a world map, featuring interactive attack vectors, threat statistics, and live news updates.

## Features

- **Real-time Threat Visualization**: Live display of cyber attacks on a world map
- **Interactive Attack Vectors**: Animated attack paths between source and target countries
- **Threat Statistics**: Real-time statistics and breakdowns of cyber attacks
- **Live News Feed**: Animated news feed with real-time updates
- **Severity Filtering**: Filter attacks by severity level
- **Responsive Design**: Modern UI with smooth animations and transitions
- **Web Worker Support**: Efficient threat processing using Web Workers
- **Server-Sent Events**: Real-time data updates using SSE

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- React (v16.8 or higher)
- TypeScript

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/Deepcytes-LCTM-v2.git
cd Deepcytes-LCTM-v2
```

2. Install dependencies:

```bash
npm install
# or
yarn install
```

3. Start the development server:

```bash
npm run dev
# or
yarn dev
```

## Usage

The application consists of several key components:

```tsx
import { App } from "./App";

function Main() {
  return (
    <div>
      <App />
    </div>
  );
}
```

### Key Components

| Component  | Description                                       |
| ---------- | ------------------------------------------------- |
| WorldMap   | Displays the world map with attack vectors        |
| Stats      | Shows attack statistics and breakdowns            |
| News       | Displays real-time cyber security news            |
| Controls   | Provides play/pause and severity filtering        |
| AttackInfo | Shows detailed information about selected attacks |

## Features in Detail

### Threat Visualization

- Real-time attack vectors between countries
- Severity-based color coding
- Interactive country hover information
- Malicious IP markers

### Statistics Panel

- Total attack count
- Severity distribution
- Top source/target countries
- Attack type breakdown

### News Feed

- Real-time cyber security news
- Flip card animations
- Pagination support
- Title truncation for long headlines

### Controls

- Play/Pause threat visualization
- Severity level filtering
- Attack speed control
- Clear visualization option

## Development

### Project Structure

```
src/
  ├── components/
  │   ├── WorldMap.tsx    # World map visualization
  │   ├── Stats.tsx       # Statistics panel
  │   ├── News.tsx        # News feed component
  │   ├── Controls.tsx    # Control panel
  │   └── AttackInfo.tsx  # Attack details panel
  ├── data/
  │   ├── maliciousIPs.ts # Malicious IP handling
  │   ├── threatData.ts   # Threat data processing
  │   └── sseNews.ts      # News data handling
  ├── workers/
  │   └── threatWorker.ts # Web Worker for threat processing
  └── types/
      └── index.ts        # TypeScript type definitions
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- React team for the amazing framework
- Tailwind CSS for the utility-first CSS framework
- Contributors and maintainers of the project
