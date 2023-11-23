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
                pks = []
                for attr_properties in self.db_dict[table]['attributes']: #In 0 name, in 1 type and in 2 Constraint
                    attrs.append(attr_properties[0])
                    attrs.append(attr_properties[1])
                    if len(attr_properties) == 3:
                        attrs.append(attr_properties[2])
                        if attr_properties[2] in ['PRIMARY KEY', 'PK FK']:
                            pks.append(attr_properties[0])
                    else:
                        attrs.append('Constraint_Not_Specified')
                query = """MERGE (:Table {name:$table, attributes: $attr_list, pks:$pks})"""
                session.run(query, parameters={'table':table, 'attr_list': attrs, 'pks': pks})
                
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

        join_graph = DiGraph()
        query = """MATCH (t1:Table) RETURN t1"""
        tables,_,_ = driver.execute_query(query,database_='neo4j')

        #Graph Nodes
        for table in tables:
            atributes = []
            pks = []
            for i in range(0, len(table['t1']['attributes']), 3):
                temp = []
                for j in range(i, i+3):
                    temp.append(table['t1']['attributes'][j])
                atributes.append(tuple(temp))
                if 'PRIMARY KEY' in temp or 'PK FK' in temp:
                    pks.append(temp[0])

            join_graph.add_node(table['t1']['name'], attrs = atributes, pks = pks)

        #Graph Edges
        query = """MATCH (t1:Table) -[r:HAS_FK_TO]-> (t2:Table) RETURN t1.name, r, t2.name"""
        edges,_,_ = driver.execute_query(query, database_='neo4j')

        for edge in edges:
            t1 = edge[0]
            t2 = edge[2]
            if join_graph.has_edge(t1, t2):
                join_graph.edges[t1, t2]['conditions'].append((edge['r']['foreign_key'], edge['r']['referenced_attr']))

            else:
                join_graph.add_edge(t1, t2, 
                                    conditions = [(edge['r']['foreign_key'], edge['r']['referenced_attr'])], 
                                    weight = 1)

        #Additional Edges
        query = """MATCH (t1:Table) -[r1:HAS_FK_TO]-> (t2:Table) <-[r2:HAS_FK_TO]- (t3:Table)
                   WHERE r1.referenced_attr = r2.referenced_attr AND r2.foreign_key IN t3.pks
                   RETURN t1.name, t3.name, r1.foreign_key, r2.foreign_key"""
        
        edges,_,_ = driver.execute_query(query, database_='neo4j')

        for edge in edges:
            t1 = edge[0]
            t2 = edge[1]
            if join_graph.has_edge(t1, t2):
                join_graph.edges[t1, t2]['conditions'].append((edge[2], edge[3]))
            
            else:
                join_graph.add_edge(t1, t2, 
                                    conditions = [(edge[2], edge[3])], 
                                    weight = 1)
