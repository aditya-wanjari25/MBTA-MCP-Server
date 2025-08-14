# MBTA-MCP-Server

This is a MCP server that provides real-time train arrival predictions for MBTA stations through Claude Desktop as the MCP Client.

## What is MBTA?

The **Massachusetts Bay Transportation Authority (MBTA)** is the public transit system serving the Greater Boston area in Massachusetts. Commonly known as "the T," it operates subway lines (Red, Blue, Green, and Orange), buses, commuter rail, and ferry services. This MCP server focuses on subway/rail predictions, helping you know exactly when the next trains will arrive at any station.

## Features

- 🚇 Real-time train arrival predictions for any MBTA station
- ⏰ Shows next two upcoming trains with arrival times
- 🧭 Supports all platforms/directions at each station
- 💬 Natural language responses through Claude Desktop


## Installation

### Step 1: Install Claude Desktop

1. Download Claude Desktop from [Claude's official website](https://claude.ai/download)
2. Install and launch the application

### Step 2: Install uv (Python Package Manager)

#### On macOS and Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### On Windows:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 3: Set Up the Project

1. Clone or download this repository to your local machine
2. Navigate to the project directory
3. Install dependencies using uv:

```bash
cd path/to/your/mbta-mcp-project
uv sync
```

### Step 4: Configure Claude Desktop

You need to add the MCP server configuration to Claude Desktop's configuration file.

#### Find your configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Add the configuration:

Open the `claude_desktop_config.json` file and add the following configuration (update the paths to match your system):

```json
{
  "mcpServers": {
    "predictTrains": {
      "command": "/Users/yourusername/.local/bin/uv",
      "args": [
        "--directory",
        "/path/to/your/mbta-mcp-project",
        "run",
        "server_predict_trains.py"
      ]
    }
  }
}
```

**Important**: Replace the paths with your actual paths:
- Update `/Users/yourusername/.local/bin/uv` with the full path to your uv installation
- Update `/path/to/your/mbta-mcp-project` with the full path to where you placed this project

#### Finding your uv path:
```bash
which uv
```

### Step 5: Required Files

Make sure you have the `filtered_stops.json` file in your project directory. This file contains the MBTA station data that the server uses to look up platform IDs.

### Step 6: Restart Claude Desktop

After updating the configuration file, restart Claude Desktop for the changes to take effect.

## Usage

Once everything is set up, you can ask Claude about MBTA train predictions directly in your conversations:


<img width="1016" height="746" alt="Screenshot 2025-08-14 at 17 13 19" src="https://github.com/user-attachments/assets/a0b6b36b-e7c1-4bd6-8c0f-bbd8ee697410" />

<img width="1016" height="746" alt="Screenshot 2025-08-14 at 17 14 48" src="https://github.com/user-attachments/assets/6d82c8ce-7028-45fe-b7c3-64c6e1aef7b3" />



### **Happy commuting! 🚇**
