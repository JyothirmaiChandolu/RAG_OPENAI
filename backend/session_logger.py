"""Session logging for Kashmir Tourism RAG Chatbot - Token tracking only."""
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import json
import tiktoken


class RAGSessionLogger:
    """Manages logging for each chat session - tracks tokens only"""
    
    def __init__(self, base_log_dir: str = "logs", 
                 author: str = "Jyothirmai Chandolu",
                 employee_id: str = "800342",
                 project_name: str = "Kashmir Tourism RAG Chatbot",
                 project_description: str = "RAG-based conversational AI for Kashmir tourism information"):
        self.base_log_dir = Path(base_log_dir)
        self.session_id = None
        self.log_file_path = None
        self.logger = None
        self.author = author
        self.employee_id = employee_id
        self.project_name = project_name
        self.project_description = project_description
        
        # Initialize tokenizer for GPT-3.5
        try:
            self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        except:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        self.stats = {
            "total_query_tokens": 0,
            "total_response_tokens": 0,
            "total_session_tokens": 0,
            "queries": [],  # List of {query_tokens, response_tokens, timestamp}
            "start_time": None,
            "end_time": None,
            "session_ended": False,  # Flag to prevent multiple footer writes
        }
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            return len(self.tokenizer.encode(text))
        except:
            # Fallback approximation
            return len(text.split()) * 1.3
    
    def _write_header(self):
        """Write header to log file"""
        now = datetime.now()
        
        header = "===============================================\n"
        header += "       KASHMIR TOURISM CHATBOT SESSION\n"
        header += "===============================================\n"
        header += f"Author Name        : {self.author}\n"
        header += f"Employee ID        : {self.employee_id}\n"
        header += f"Project Name       : {self.project_name}\n"
        header += f"Project Description: {self.project_description}\n"
        header += f"Log Session ID     : {self.session_id}\n"
        header += f"Date Created       : {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
        header += "===============================================\n\n"
        
        with open(self.log_file_path, "w", encoding='utf-8') as f:
            f.write(header)
    
    def _write_footer(self, error: Optional[str] = None):
        """Write footer to log file"""
        try:
            footer = "\n\n===============================================\n"
            footer += "          SESSION STATISTICS\n"
            footer += "===============================================\n"
            
            if error:
                footer += f"\n⚠️ SESSION ENDED WITH ERROR:\n{error}\n\n"
            else:
                footer += "\n✅ SESSION COMPLETED SUCCESSFULLY\n\n"
            
            footer += "TOKEN USAGE SUMMARY:\n"
            footer += "-----------------------------------------------\n"
            footer += f"Total Query Tokens    : {self.stats['total_query_tokens']}\n"
            footer += f"Total Response Tokens : {self.stats['total_response_tokens']}\n"
            footer += f"Total Session Tokens  : {self.stats['total_session_tokens']}\n"
            footer += f"Number of Queries     : {len(self.stats['queries'])}\n\n"
            
            footer += "TIMING INFORMATION:\n"
            footer += "-----------------------------------------------\n"
            if self.stats['start_time']:
                footer += f"Start Time         : {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            if self.stats['end_time']:
                footer += f"End Time           : {self.stats['end_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
                footer += f"Duration           : {duration:.2f} seconds\n\n"
            
            footer += "===============================================\n"
            footer += f"Log File Path      : {self.log_file_path}\n"
            footer += f"Session ID         : {self.session_id}\n"
            footer += "===============================================\n"
            footer += "           PROJECT LOG END\n"
            footer += "===============================================\n"
            
            with open(self.log_file_path, "a", encoding='utf-8') as f:
                f.write(footer)
            
            print(f"Footer written and logger closed for session: {self.session_id}")
            
        except Exception as e:
            print(f"ERROR: Failed to write footer: {e}")
    
    def start_session(self) -> str:
        """Start a new chat session with logging"""
        # Generate unique session ID (8 character UUID)
        self.session_id = uuid.uuid4().hex[:8]
        self.stats["start_time"] = datetime.now()
        
        # Create log directory structure: logs/year/month/day/
        now = datetime.now()
        Year_stamp = now.strftime("%Y")
        Month_stamp = now.strftime("%m")
        Day_stamp = now.strftime("%d")
        Day_folder = self.base_log_dir / Year_stamp / Month_stamp / Day_stamp
        Day_folder.mkdir(parents=True, exist_ok=True)
        
        # Create log file with session ID
        self.log_file_path = Day_folder / f"chat_session_{self.session_id}.log"
        
        # Write header first
        self._write_header()
        
        # Setup logger for this session
        self.logger = logging.getLogger(f"rag_session_{self.session_id}")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self.logger.handlers.clear()
        
        # File handler - append mode since header is already written
        file_handler = logging.FileHandler(self.log_file_path, mode='a', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Log session start
        self.logger.info("=" * 80)
        self.logger.info("CHAT SESSION STARTED")
        self.logger.info("=" * 80)
        self.logger.info("")
        
        print(f"Log file ID  : {self.session_id}")
        print(f"Log file path: {self.log_file_path}")
        
        return self.session_id
    
    def log_query_response(self, query: str, response: str, success: bool = True):
        """Log a successful query-response pair with token counts"""
        if not success:
            return  # Only log successful responses
        
        query_tokens = self._count_tokens(query)
        response_tokens = self._count_tokens(response)
        total_tokens = query_tokens + response_tokens
        
        # Update stats
        self.stats["total_query_tokens"] += query_tokens
        self.stats["total_response_tokens"] += response_tokens
        self.stats["total_session_tokens"] += total_tokens
        
        self.stats["queries"].append({
            "query_tokens": query_tokens,
            "response_tokens": response_tokens,
            "total_tokens": total_tokens,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Log to file
        if self.logger:
            self.logger.info("-" * 80)
            self.logger.info(f"Query Tokens    : {query_tokens}")
            self.logger.info(f"Response Tokens : {response_tokens}")
            self.logger.info(f"Total Tokens    : {total_tokens}")
            self.logger.info("-" * 80)
            self.logger.info("")
    
    def end_session(self, error: Optional[str] = None):
        """End the chat session and write footer with statistics"""
        # Check if already ended to prevent multiple footer writes
        if self.stats.get("session_ended", False):
            return
        
        self.stats["session_ended"] = True
        self.stats["end_time"] = datetime.now()
        
        if self.logger:
            self.logger.info("")
            self.logger.info("=" * 80)
            self.logger.info("CHAT SESSION COMPLETED")
            self.logger.info("=" * 80)
            
            if error:
                self.logger.error(f"Session ended with error: {error}")
            
            # Close all handlers before writing footer
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)
        
        # Write footer to file
        self._write_footer(error)
        
        # Save stats as JSON for easy parsing
        stats_file = self.log_file_path.with_suffix('.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            stats_dict = {
                "session_id": self.session_id,
                "author": self.author,
                "employee_id": self.employee_id,
                "project_name": self.project_name,
                "start_time": self.stats["start_time"].isoformat() if self.stats["start_time"] else None,
                "end_time": self.stats["end_time"].isoformat() if self.stats["end_time"] else None,
                "total_query_tokens": self.stats["total_query_tokens"],
                "total_response_tokens": self.stats["total_response_tokens"],
                "total_session_tokens": self.stats["total_session_tokens"],
                "number_of_queries": len(self.stats["queries"]),
                "queries": self.stats["queries"],
                "error": error
            }
            json.dump(stats_dict, f, indent=2)
    
    def get_stats(self) -> Dict:
        """Get current statistics"""
        return self.stats.copy()
    
    def get_log_path(self) -> Optional[Path]:
        """Get the path to the log file"""
        return self.log_file_path


_current_session_logger: Optional[RAGSessionLogger] = None

def get_session_logger() -> Optional[RAGSessionLogger]:
    """Get the current session logger"""
    return _current_session_logger

def set_session_logger(logger: Optional[RAGSessionLogger]):
    """Set the current session logger"""
    global _current_session_logger
    _current_session_logger = logger

def create_session_logger(base_log_dir: str = "logs",
                         author: str = "Jyothirmai Chandolu",
                         employee_id: str = "800342",
                         project_name: str = "Kashmir Tourism RAG Chatbot",
                         project_description: str = "RAG-based conversational AI for Kashmir tourism information") -> RAGSessionLogger:
    """Create a new session logger with custom project details"""
    return RAGSessionLogger(base_log_dir, author, employee_id, project_name, project_description)