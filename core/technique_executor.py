"""
Technique executor with safe execution
"""

import subprocess
import logging
from typing import Dict, Optional
from .exceptions import TechniqueExecutionError

logger = logging.getLogger(__name__)


class TechniqueExecutor:
    """Executes techniques with safety controls"""
    
    def __init__(self, safe_mode: bool = True, timeout: int = 30):
        self.safe_mode = safe_mode
        self.timeout = timeout
        self.executed_commands = []
        
    def execute(self, command: str, technique_name: str) -> Dict:
        """Execute a command safely"""
        
        if self.safe_mode:
            logger.warning(f"SAFE MODE: Would execute: {command}")
            # In safe mode, just log the command
            return {
                'success': True,
                'output': f"[SAFE MODE] Would execute: {command}",
                'error': None
            }
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            self.executed_commands.append({
                'command': command,
                'technique': technique_name,
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            })
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
            
        except subprocess.TimeoutExpired:
            raise TechniqueExecutionError(f"Command timed out after {self.timeout}s")
        except Exception as e:
            raise TechniqueExecutionError(f"Execution failed: {e}")
    
    def get_history(self):
        """Get execution history"""
        return self.executed_commands
