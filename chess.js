// Chess Game Implementation
class ChessGame {
    constructor() {
        this.board = this.initializeBoard();
        this.currentPlayer = 'white';
        this.selectedSquare = null;
        this.gameStatus = 'active';
        this.moveHistory = [];
        this.enPassantTarget = null;
        this.castlingRights = {
            white: { kingside: true, queenside: true },
            black: { kingside: true, queenside: true }
        };
        this.kingPositions = { white: [7, 4], black: [0, 4] };
        
        this.pieces = {
            white: {
                king: '♔', queen: '♕', rook: '♖', 
                bishop: '♗', knight: '♘', pawn: '♙'
            },
            black: {
                king: '♚', queen: '♛', rook: '♜', 
                bishop: '♝', knight: '♞', pawn: '♟'
            }
        };
        
        this.initializeGame();
    }

    initializeBoard() {
        const board = Array(8).fill(null).map(() => Array(8).fill(null));
        
        // Set up initial positions
        const initialSetup = [
            ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'],
            ['pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        ];
        
        // Black pieces
        for (let col = 0; col < 8; col++) {
            board[0][col] = { type: initialSetup[0][col], color: 'black' };
            board[1][col] = { type: initialSetup[1][col], color: 'black' };
        }
        
        // White pieces
        for (let col = 0; col < 8; col++) {
            board[6][col] = { type: initialSetup[1][col], color: 'white' };
            board[7][col] = { type: initialSetup[0][col], color: 'white' };
        }
        
        return board;
    }

    initializeGame() {
        this.createBoard();
        this.updateGameInfo();
    }

    createBoard() {
        const boardElement = document.getElementById('chess-board');
        boardElement.innerHTML = '';
        
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const square = document.createElement('div');
                square.className = `square ${(row + col) % 2 === 0 ? 'light' : 'dark'}`;
                square.dataset.row = row;
                square.dataset.col = col;
                square.addEventListener('click', () => this.handleSquareClick(row, col));
                
                const piece = this.board[row][col];
                if (piece) {
                    const pieceElement = document.createElement('span');
                    pieceElement.className = 'piece';
                    pieceElement.textContent = this.pieces[piece.color][piece.type];
                    square.appendChild(pieceElement);
                }
                
                boardElement.appendChild(square);
            }
        }
    }

    handleSquareClick(row, col) {
        if (this.gameStatus !== 'active') return;
        
        const clickedSquare = [row, col];
        const piece = this.board[row][col];
        
        if (this.selectedSquare) {
            if (this.selectedSquare[0] === row && this.selectedSquare[1] === col) {
                // Deselect current square
                this.clearSelection();
                return;
            }
            
            // Try to make a move
            if (this.isValidMove(this.selectedSquare, clickedSquare)) {
                this.makeMove(this.selectedSquare, clickedSquare);
                this.clearSelection();
                this.switchPlayer();
                this.updateGameInfo();
                this.checkGameStatus();
            } else {
                // Select new piece if it belongs to current player
                if (piece && piece.color === this.currentPlayer) {
                    this.selectSquare(row, col);
                } else {
                    this.clearSelection();
                }
            }
        } else {
            // Select piece if it belongs to current player
            if (piece && piece.color === this.currentPlayer) {
                this.selectSquare(row, col);
            }
        }
    }

    selectSquare(row, col) {
        this.clearSelection();
        this.selectedSquare = [row, col];
        
        const square = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        square.classList.add('selected');
        
        // Highlight possible moves
        this.highlightPossibleMoves(row, col);
    }

    clearSelection() {
        this.selectedSquare = null;
        document.querySelectorAll('.square').forEach(square => {
            square.classList.remove('selected', 'possible-move', 'capture-move');
        });
    }

    highlightPossibleMoves(row, col) {
        const possibleMoves = this.getPossibleMoves(row, col);
        
        possibleMoves.forEach(([moveRow, moveCol]) => {
            const square = document.querySelector(`[data-row="${moveRow}"][data-col="${moveCol}"]`);
            if (this.board[moveRow][moveCol]) {
                square.classList.add('capture-move');
            } else {
                square.classList.add('possible-move');
            }
        });
    }

    getPossibleMoves(row, col) {
        const piece = this.board[row][col];
        if (!piece) return [];
        
        let moves = [];
        
        switch (piece.type) {
            case 'pawn':
                moves = this.getPawnMoves(row, col, piece.color);
                break;
            case 'rook':
                moves = this.getRookMoves(row, col, piece.color);
                break;
            case 'knight':
                moves = this.getKnightMoves(row, col, piece.color);
                break;
            case 'bishop':
                moves = this.getBishopMoves(row, col, piece.color);
                break;
            case 'queen':
                moves = this.getQueenMoves(row, col, piece.color);
                break;
            case 'king':
                moves = this.getKingMoves(row, col, piece.color);
                break;
        }
        
        // Filter out moves that would put own king in check
        return moves.filter(move => !this.wouldBeInCheck(piece.color, [row, col], move));
    }

    getPawnMoves(row, col, color) {
        const moves = [];
        const direction = color === 'white' ? -1 : 1;
        const startRow = color === 'white' ? 6 : 1;
        
        // Forward move
        if (this.isInBounds(row + direction, col) && !this.board[row + direction][col]) {
            moves.push([row + direction, col]);
            
            // Double move from starting position
            if (row === startRow && !this.board[row + 2 * direction][col]) {
                moves.push([row + 2 * direction, col]);
            }
        }
        
        // Captures
        for (const colOffset of [-1, 1]) {
            const newRow = row + direction;
            const newCol = col + colOffset;
            
            if (this.isInBounds(newRow, newCol)) {
                const targetPiece = this.board[newRow][newCol];
                if (targetPiece && targetPiece.color !== color) {
                    moves.push([newRow, newCol]);
                }
                
                // En passant
                if (this.enPassantTarget && 
                    this.enPassantTarget[0] === newRow && 
                    this.enPassantTarget[1] === newCol) {
                    moves.push([newRow, newCol]);
                }
            }
        }
        
        return moves;
    }

    getRookMoves(row, col, color) {
        const moves = [];
        const directions = [[0, 1], [0, -1], [1, 0], [-1, 0]];
        
        for (const [dRow, dCol] of directions) {
            for (let i = 1; i < 8; i++) {
                const newRow = row + i * dRow;
                const newCol = col + i * dCol;
                
                if (!this.isInBounds(newRow, newCol)) break;
                
                const targetPiece = this.board[newRow][newCol];
                if (!targetPiece) {
                    moves.push([newRow, newCol]);
                } else {
                    if (targetPiece.color !== color) {
                        moves.push([newRow, newCol]);
                    }
                    break;
                }
            }
        }
        
        return moves;
    }

    getKnightMoves(row, col, color) {
        const moves = [];
        const knightMoves = [
            [-2, -1], [-2, 1], [-1, -2], [-1, 2],
            [1, -2], [1, 2], [2, -1], [2, 1]
        ];
        
        for (const [dRow, dCol] of knightMoves) {
            const newRow = row + dRow;
            const newCol = col + dCol;
            
            if (this.isInBounds(newRow, newCol)) {
                const targetPiece = this.board[newRow][newCol];
                if (!targetPiece || targetPiece.color !== color) {
                    moves.push([newRow, newCol]);
                }
            }
        }
        
        return moves;
    }

    getBishopMoves(row, col, color) {
        const moves = [];
        const directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]];
        
        for (const [dRow, dCol] of directions) {
            for (let i = 1; i < 8; i++) {
                const newRow = row + i * dRow;
                const newCol = col + i * dCol;
                
                if (!this.isInBounds(newRow, newCol)) break;
                
                const targetPiece = this.board[newRow][newCol];
                if (!targetPiece) {
                    moves.push([newRow, newCol]);
                } else {
                    if (targetPiece.color !== color) {
                        moves.push([newRow, newCol]);
                    }
                    break;
                }
            }
        }
        
        return moves;
    }

    getQueenMoves(row, col, color) {
        return [...this.getRookMoves(row, col, color), ...this.getBishopMoves(row, col, color)];
    }

    getKingMoves(row, col, color) {
        const moves = [];
        const directions = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1],           [0, 1],
            [1, -1],  [1, 0],  [1, 1]
        ];
        
        for (const [dRow, dCol] of directions) {
            const newRow = row + dRow;
            const newCol = col + dCol;
            
            if (this.isInBounds(newRow, newCol)) {
                const targetPiece = this.board[newRow][newCol];
                if (!targetPiece || targetPiece.color !== color) {
                    moves.push([newRow, newCol]);
                }
            }
        }
        
        // Castling
        if (!this.isInCheck(color)) {
            // Kingside castling
            if (this.castlingRights[color].kingside && 
                !this.board[row][col + 1] && !this.board[row][col + 2] &&
                !this.wouldBeInCheck(color, [row, col], [row, col + 1]) &&
                !this.wouldBeInCheck(color, [row, col], [row, col + 2])) {
                moves.push([row, col + 2]);
            }
            
            // Queenside castling
            if (this.castlingRights[color].queenside && 
                !this.board[row][col - 1] && !this.board[row][col - 2] && !this.board[row][col - 3] &&
                !this.wouldBeInCheck(color, [row, col], [row, col - 1]) &&
                !this.wouldBeInCheck(color, [row, col], [row, col - 2])) {
                moves.push([row, col - 2]);
            }
        }
        
        return moves;
    }

    isInBounds(row, col) {
        return row >= 0 && row < 8 && col >= 0 && col < 8;
    }

    isValidMove(from, to) {
        const possibleMoves = this.getPossibleMoves(from[0], from[1]);
        return possibleMoves.some(move => move[0] === to[0] && move[1] === to[1]);
    }

    makeMove(from, to) {
        const [fromRow, fromCol] = from;
        const [toRow, toCol] = to;
        const piece = this.board[fromRow][fromCol];
        const capturedPiece = this.board[toRow][toCol];
        
        // Store move for history
        const moveNotation = this.getMoveNotation(from, to, piece, capturedPiece);
        
        // Handle special moves
        this.handleSpecialMoves(from, to, piece);
        
        // Make the move
        this.board[toRow][toCol] = piece;
        this.board[fromRow][fromCol] = null;
        
        // Update king position
        if (piece.type === 'king') {
            this.kingPositions[piece.color] = [toRow, toCol];
        }
        
        // Add move to history
        this.moveHistory.push({
            from, to, piece, capturedPiece, notation: moveNotation
        });
        
        // Update move list display
        this.updateMoveList();
        
        // Recreate board to reflect changes
        this.createBoard();
    }

    handleSpecialMoves(from, to, piece) {
        const [fromRow, fromCol] = from;
        const [toRow, toCol] = to;
        
        // En passant capture
        if (piece.type === 'pawn' && this.enPassantTarget && 
            toRow === this.enPassantTarget[0] && toCol === this.enPassantTarget[1]) {
            const capturedPawnRow = piece.color === 'white' ? toRow + 1 : toRow - 1;
            this.board[capturedPawnRow][toCol] = null;
        }
        
        // Set en passant target for next turn
        this.enPassantTarget = null;
        if (piece.type === 'pawn' && Math.abs(toRow - fromRow) === 2) {
            this.enPassantTarget = [fromRow + (toRow - fromRow) / 2, fromCol];
        }
        
        // Castling
        if (piece.type === 'king' && Math.abs(toCol - fromCol) === 2) {
            const rookFromCol = toCol > fromCol ? 7 : 0;
            const rookToCol = toCol > fromCol ? toCol - 1 : toCol + 1;
            
            this.board[toRow][rookToCol] = this.board[toRow][rookFromCol];
            this.board[toRow][rookFromCol] = null;
        }
        
        // Update castling rights
        if (piece.type === 'king') {
            this.castlingRights[piece.color].kingside = false;
            this.castlingRights[piece.color].queenside = false;
        } else if (piece.type === 'rook') {
            if (fromCol === 0) {
                this.castlingRights[piece.color].queenside = false;
            } else if (fromCol === 7) {
                this.castlingRights[piece.color].kingside = false;
            }
        }
        
        // Pawn promotion
        if (piece.type === 'pawn' && (toRow === 0 || toRow === 7)) {
            // For simplicity, always promote to queen
            this.board[toRow][toCol] = { type: 'queen', color: piece.color };
        }
    }

    getMoveNotation(from, to, piece, capturedPiece) {
        const [fromRow, fromCol] = from;
        const [toRow, toCol] = to;
        
        const files = 'abcdefgh';
        const fromSquare = files[fromCol] + (8 - fromRow);
        const toSquare = files[toCol] + (8 - toRow);
        
        let notation = '';
        
        if (piece.type === 'pawn') {
            if (capturedPiece) {
                notation = files[fromCol] + 'x' + toSquare;
            } else {
                notation = toSquare;
            }
        } else {
            const pieceSymbol = piece.type.charAt(0).toUpperCase();
            notation = pieceSymbol + (capturedPiece ? 'x' : '') + toSquare;
        }
        
        return notation;
    }

    isInCheck(color) {
        const kingPos = this.kingPositions[color];
        const opponentColor = color === 'white' ? 'black' : 'white';
        
        // Check if any opponent piece can attack the king
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const piece = this.board[row][col];
                if (piece && piece.color === opponentColor) {
                    const moves = this.getPossibleMovesWithoutCheckValidation(row, col, piece.color);
                    if (moves.some(move => move[0] === kingPos[0] && move[1] === kingPos[1])) {
                        return true;
                    }
                }
            }
        }
        
        return false;
    }

    getPossibleMovesWithoutCheckValidation(row, col, color) {
        const piece = this.board[row][col];
        if (!piece) return [];
        
        switch (piece.type) {
            case 'pawn': return this.getPawnMoves(row, col, color);
            case 'rook': return this.getRookMoves(row, col, color);
            case 'knight': return this.getKnightMoves(row, col, color);
            case 'bishop': return this.getBishopMoves(row, col, color);
            case 'queen': return this.getQueenMoves(row, col, color);
            case 'king': return this.getKingMoves(row, col, color).filter(move => Math.abs(move[1] - col) <= 1); // Exclude castling
            default: return [];
        }
    }

    wouldBeInCheck(color, from, to) {
        // Simulate the move
        const [fromRow, fromCol] = from;
        const [toRow, toCol] = to;
        const originalPiece = this.board[toRow][toCol];
        const movingPiece = this.board[fromRow][fromCol];
        
        this.board[toRow][toCol] = movingPiece;
        this.board[fromRow][fromCol] = null;
        
        // Update king position temporarily if moving king
        const originalKingPos = [...this.kingPositions[color]];
        if (movingPiece && movingPiece.type === 'king') {
            this.kingPositions[color] = [toRow, toCol];
        }
        
        const inCheck = this.isInCheck(color);
        
        // Restore board state
        this.board[fromRow][fromCol] = movingPiece;
        this.board[toRow][toCol] = originalPiece;
        this.kingPositions[color] = originalKingPos;
        
        return inCheck;
    }

    checkGameStatus() {
        const currentPlayerHasMoves = this.hasValidMoves(this.currentPlayer);
        const inCheck = this.isInCheck(this.currentPlayer);
        
        if (!currentPlayerHasMoves) {
            if (inCheck) {
                this.gameStatus = 'checkmate';
                const winner = this.currentPlayer === 'white' ? 'Black' : 'White';
                document.getElementById('game-status').textContent = `Checkmate! ${winner} wins!`;
                document.getElementById('game-status').style.color = '#dc3545';
            } else {
                this.gameStatus = 'stalemate';
                document.getElementById('game-status').textContent = 'Stalemate! Draw!';
                document.getElementById('game-status').style.color = '#ffc107';
            }
        } else if (inCheck) {
            document.getElementById('game-status').textContent = 'Check!';
            document.getElementById('game-status').style.color = '#fd7e14';
            
            // Highlight king in check
            const kingPos = this.kingPositions[this.currentPlayer];
            const kingSquare = document.querySelector(`[data-row="${kingPos[0]}"][data-col="${kingPos[1]}"]`);
            kingSquare.classList.add('in-check');
        } else {
            document.getElementById('game-status').textContent = 'Game in Progress';
            document.getElementById('game-status').style.color = '#28a745';
        }
    }

    hasValidMoves(color) {
        for (let row = 0; row < 8; row++) {
            for (let col = 0; col < 8; col++) {
                const piece = this.board[row][col];
                if (piece && piece.color === color) {
                    const moves = this.getPossibleMoves(row, col);
                    if (moves.length > 0) {
                        return true;
                    }
                }
            }
        }
        return false;
    }

    switchPlayer() {
        this.currentPlayer = this.currentPlayer === 'white' ? 'black' : 'white';
    }

    updateGameInfo() {
        const playerText = this.currentPlayer === 'white' ? "White's Turn" : "Black's Turn";
        document.getElementById('current-player').textContent = playerText;
        
        // Remove check highlighting from previous turn
        document.querySelectorAll('.in-check').forEach(square => {
            square.classList.remove('in-check');
        });
    }

    updateMoveList() {
        const moveList = document.getElementById('move-list');
        const lastMove = this.moveHistory[this.moveHistory.length - 1];
        
        if (lastMove) {
            const moveEntry = document.createElement('div');
            moveEntry.className = 'move-entry';
            const moveNumber = Math.ceil(this.moveHistory.length / 2);
            const color = this.moveHistory.length % 2 === 1 ? 'White' : 'Black';
            moveEntry.textContent = `${moveNumber}. ${color}: ${lastMove.notation}`;
            moveList.appendChild(moveEntry);
            moveList.scrollTop = moveList.scrollHeight;
        }
    }
}

// Global game instance
let game;

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    startNewGame();
});

function startNewGame() {
    game = new ChessGame();
    document.getElementById('move-list').innerHTML = '';
}

function undoMove() {
    if (game.moveHistory.length === 0) return;
    
    const lastMove = game.moveHistory.pop();
    const { from, to, piece, capturedPiece } = lastMove;
    
    // Restore the move
    game.board[from[0]][from[1]] = piece;
    game.board[to[0]][to[1]] = capturedPiece;
    
    // Update king position if necessary
    if (piece.type === 'king') {
        game.kingPositions[piece.color] = from;
    }
    
    // Switch back to previous player
    game.switchPlayer();
    
    // Remove last move from display
    const moveList = document.getElementById('move-list');
    if (moveList.lastChild) {
        moveList.removeChild(moveList.lastChild);
    }
    
    // Reset game status if it was ended
    if (game.gameStatus !== 'active') {
        game.gameStatus = 'active';
    }
    
    // Recreate board and update info
    game.createBoard();
    game.updateGameInfo();
    game.checkGameStatus();
}
