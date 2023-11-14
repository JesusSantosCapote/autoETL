from crawler.crawler import Crawler
from logger import logger
import psycopg2
from psycopg2 import sql
import json
import os


class PostgreSqlCrawler(Crawler):
    def __init__(self, db_params) -> None:
        super().__init__(db_params)
        
    
    def explore_db(self):
        connection = psycopg2.connect(**self._db_params)
        cursor = connection.cursor()

        # Database table list
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        table_names = cursor.fetchall()

        for table_name in table_names:
            table_info = {
                'attributes': [],
                'relations': []
            }
            self._metadata_str.join(f"Table: {table_name[0]}\n")

            # Get table column information
            cursor.execute(sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s"),
                        [table_name[0]])
            columns = cursor.fetchall()

            for column in columns:
                table_info['attributes'].append((column[0], column[1]))
                self._metadata_str.join(f"  Column: {column[0]} - Type: {column[1]}\n")

            # Get the foreign keys of the table
            cursor.execute(sql.SQL("""
                SELECT 
                    conname AS foreign_key_name,
                    conrelid::regclass AS table_name,
                    a.attname AS column_name,
                    confrelid::regclass AS referenced_table_name,
                    af.attname AS referenced_column_name
                FROM 
                    pg_constraint AS c
                    JOIN pg_attribute AS a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
                    JOIN pg_attribute AS af ON af.attnum = ANY(c.confkey) AND af.attrelid = c.confrelid
                WHERE 
                    c.contype = 'f' 
                    AND c.conrelid = %s::regclass;
            """), [table_name[0]])
            foreign_keys = cursor.fetchall()

            for foreign_key in foreign_keys:
                fk_to_save = (foreign_key[2], foreign_key[3], foreign_key[4])
                from_elements = [tupla[0] for tupla in table_info['relations']]
                to_elements = [tupla[2] for tupla in table_info['relations']]
                if fk_to_save[0] not in from_elements and fk_to_save[2] not in to_elements:
                    table_info['relations'].append(fk_to_save)
                    self._metadata_str.join(
                        f"  Foreign Key: {foreign_key[0]} - Table Name: {foreign_key[1]} - Column Name: {foreign_key[2]} - "
                        f"Referenced Table Name: {foreign_key[3]} - Referenced Column Name: {foreign_key[4]}\n")

            self._db_dict[table_name[0]] = table_info
            self._metadata_str.join('\n')

        cursor.close()
        connection.close()

        path = os.path.join(os.getcwd(), 'crawler', 'data', f"{self._db_params['dbname']}_schema.json")

        with open(path, 'w') as json_file:
            json.dump(self._db_dict, json_file, indent=4)


    def get_db_dict(self):
        return self._db_dict
    

    def export_metadata_to_file(self):
        path = os.path.join(os.getcwd(), 'crawler', 'data', f"{self._db_params['dbname']}_metadata.txt")
        with open(path) as file:
            try:
                file.write(self._metadata_str)
                logger.info('Metadata exported correctly')
            except:
                logger.error('Unable to write metadata to the file')
