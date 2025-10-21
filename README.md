# ♔ Chess Game ♛

A fully functional, interactive chess game built with HTML, CSS, and JavaScript. Play chess directly in your web browser with a beautiful, responsive interface.

## 🎮 Features

### Core Chess Functionality
- **Complete Chess Rules**: All standard chess rules implemented including:
  - Piece movement validation for all pieces (Pawn, Rook, Knight, Bishop, Queen, King)
  - Castling (both kingside and queenside)
  - En passant captures
  - Pawn promotion (automatically promotes to Queen)
  - Check and checkmate detection
  - Stalemate detection

### Interactive Interface
- **Visual Feedback**: 
  - Hover effects on pieces and squares
  - Selected piece highlighting
  - Possible move indicators (yellow for moves, red for captures)
  - Check indicator with pulsing animation
- **Move History**: Complete game notation tracking
- **Game Controls**: New game and undo move functionality

### Responsive Design
- **Mobile Friendly**: Adapts to different screen sizes
- **Beautiful Styling**: Modern gradient backgrounds and smooth animations
- **Professional Layout**: Clean, intuitive interface

## 🚀 How to Play

1. **Open the Game**: Open `index.html` in any modern web browser
2. **Make Moves**: 
   - Click on a piece to select it (pieces highlight in green)
   - Click on a highlighted square to move the piece
   - Yellow squares indicate possible moves
   - Red squares indicate capture moves
3. **Special Moves**:
   - **Castling**: Click the king, then click two squares toward the rook
   - **En Passant**: Available automatically when conditions are met
   - **Pawn Promotion**: Pawns automatically promote to Queens when reaching the end

## 🎯 Game Features

### Visual Indicators
- **Current Player**: Displays whose turn it is
- **Game Status**: Shows check, checkmate, stalemate, or game in progress
- **Move History**: Tracks all moves in standard chess notation
- **Check Warning**: King flashes red when in check

### Controls
- **New Game**: Reset the board to start over
- **Undo Move**: Take back the last move (great for learning!)

## 🛠️ Technical Implementation

### Files Structure
```
chess-game/
├── index.html      # Main HTML structure
├── styles.css      # Complete styling and animations
├── chess.js        # Full chess engine implementation
└── README.md       # This documentation
```

### Key Components
- **ChessGame Class**: Main game logic and state management
- **Move Validation**: Comprehensive rule checking for all pieces
- **Check Detection**: Prevents illegal moves that would expose the king
- **Game State Management**: Tracks castling rights, en passant, and move history

## 🎨 Customization

The game is built with clean, modular code that's easy to customize:

- **Piece Symbols**: Unicode chess pieces (can be replaced with images)
- **Color Scheme**: CSS variables for easy theme changes
- **Board Size**: Responsive grid system
- **Animations**: CSS transitions and keyframe animations

## 🔧 Browser Compatibility

Works in all modern browsers:
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 🎓 Learning Chess

This implementation follows official chess rules and is perfect for:
- Learning chess basics
- Practicing tactics
- Understanding special moves
- Studying game positions

## 🚀 Getting Started

1. Download all files to a folder
2. Open `index.html` in your web browser
3. Start playing immediately!

No installation, no dependencies, no setup required!

---

**Enjoy your game of chess!** ♔♛
