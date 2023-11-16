import neo4j
from neo4j import GraphDatabase
from logger import logger
from networkx import DiGraph

class DataCatalogHandler():
    def __init__(self, db_dict, user, password, uri) -> None:
        self.db_dict = db_dict
        self._user = user
        self._password = password
        self._uri = uri

    def create_data_catalog(self):
        driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        try:
            driver.verify_connectivity()
            logger.info('Connection with Data Catalog succefully')
        except Exception as e:
            logger.error(e)

        with driver.session(database='neo4j') as session:
            try:
                constraint = """CREATE CONSTRAINT FOR (t:Table)
                                REQUIRE t.name IS UNIQUE"""
                session.run(constraint)
            except:
                pass

            for table in self.db_dict.keys():
                attrs = [] #This is needed because neo4j dont support list of lists
                rels = []
                for attr, attr_type in self.db_dict[table]['attributes']:
                    attrs.append(attr)
                    attrs.append(attr_type)

                for fk, ref_table, ref_attr in self.db_dict[table]['relations']:
                    rels.append(fk)
                    rels.append(ref_table)
                    rels.append(ref_attr)

                query = """MERGE (:Table {name:$table, attributes: $attr_list, relations: $rel})"""
                session.run(query, parameters={'table':table, 'attr_list': attrs, 'rel': rels})
                
            for table in self.db_dict.keys():
                for fk, ref_table, ref_attr in self.db_dict[table]['relations']:
                    query = """MATCH (t1:Table {name:$t1_name}), (t2:Table {name:$t2_name})
                               MERGE (t1) -[:HAS_FK_TO {foreign_key:$fk, referenced_attr:$ra}]-> (t2)"""
                    session.run(query, parameters={'fk':fk, 'ra': ref_attr, 't1_name': table, 't2_name': ref_table})
            
            session.close()

        driver.close()


    def get_join_graph(self):
        driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        try:
            driver.verify_connectivity()
            logger.info('Connection with Data Catalog succefully')
        except Exception as e:
            logger.error(e)

        with driver.session(database='neo4j') as session:
            query = """MATCH (t1:Table) -[r1:HAS_FK_TO]"""