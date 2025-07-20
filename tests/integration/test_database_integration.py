"""Integration tests for database operations."""

import pytest
import sys
import os
from unittest.mock import Mock, patch

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


class TestDatabaseIntegration:
    """Integration tests for database functionality."""
    
    @pytest.mark.integration
    @patch('psycopg2.connect')
    def test_database_connection(self, mock_connect):
        """Test database connection integration."""
        from mri_param_analyzer.core.database import connect_to_database
        
        # Mock successful connection
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        result = connect_to_database()
        
        assert result == mock_connection
        mock_connect.assert_called_once()
        
    @pytest.mark.integration  
    @patch('psycopg2.connect')
    def test_database_table_creation(self, mock_connect):
        """Test database table creation integration."""
        from mri_param_analyzer.core.database import create_tables
        
        # Mock connection and cursor
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection
        
        create_tables(mock_connection)
        
        # Verify cursor operations were called
        assert mock_cursor.execute.called
        assert mock_cursor.close.called
        assert mock_connection.commit.called
        assert mock_connection.close.called 