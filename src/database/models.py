import sqlite3
import os
from typing import Optional, List

class Database:
    def __init__(self, db_path: str = "gitcord.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """ create tables if they don't exist """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # create guilds (server) table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guilds (
                id TEXT PRIMARY KEY,
                announcements_channel_id TEXT
            )
        ''')
        
        # create repo table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner TEXT NOT NULL,
                name TEXT NOT NULL,
                webhook_secret TEXT NOT NULL,
                guild_id TEXT NOT NULL,
                FOREIGN KEY (guild_id) REFERENCES guilds (id)
            )
        ''')
        
        # create user links table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_links (
                discord_user_id TEXT PRIMARY KEY,
                github_username TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialised successfully!")
    
    def link_user(self, discord_user_id: str, github_username: str):
        """ link a discord user to their github username"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_links (discord_user_id, github_username)
            VALUES (?, ?)
        ''', (discord_user_id, github_username))
        
        conn.commit()
        conn.close()
    
    def get_linked_github(self, discord_user_id: str) -> Optional[str]:
        """ get github username for a discord user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT github_username FROM user_links WHERE discord_user_id = ?
        ''', (discord_user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
    
    def save_repo(self, guild_id: str, owner: str, name: str, webhook_secret: str, channel_id: str):
        """ save repository configuration """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # update or create guild
        cursor.execute('''
            INSERT OR REPLACE INTO guilds (id, announcements_channel_id)
            VALUES (?, ?)
        ''', (guild_id, channel_id))
        
        # save repo
        cursor.execute('''
            INSERT INTO repos (owner, name, webhook_secret, guild_id)
            VALUES (?, ?, ?, ?)
        ''', (owner, name, webhook_secret, guild_id))
        
        conn.commit()
        conn.close()
    
    def get_repo_by_owner_name(self, owner: str, name: str) -> Optional[dict]:
        """Get repository by owner/name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.*, g.announcements_channel_id 
            FROM repos r 
            JOIN guilds g ON r.guild_id = g.id 
            WHERE r.owner = ? AND r.name = ?
        ''', (owner, name))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'owner': result[1],
                'name': result[2],
                'webhook_secret': result[3],
                'guild_id': result[4],
                'announcements_channel_id': result[5]
            }
        return None