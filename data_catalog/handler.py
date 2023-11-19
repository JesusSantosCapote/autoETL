import neo4j
from neo4j import GraphDatabase
from logger import logger
from networkx import DiGraph

tpc_h = DiGraph()
tpc_h.add_node('part', attrs=[('partkey', 'integer', 'PRIMARY KEY'), 
                              ('name', 'character varying', 'Constraint_Not_Specified'), 
                              ('brand', 'character varying', 'Constraint_Not_Specified')], pks=['partkey'])

tpc_h.add_node('supplier', attrs=[('supkey', 'integer', 'PRIMARY KEY'), 
                                  ('name', 'character varying', 'Constraint_Not_Specified'), 
                                  ('nationkey', 'integer', 'FOREIGN KEY')], pks=['supkey'])

tpc_h.add_node('partsupp', attrs=[('partkey', 'integer', 'PK FK'), 
                                  ('supkey', 'integer', 'PK FK'), 
                                  ('qty', 'integer', 'Constraint_Not_Specified')], pks=['partkey', 'supkey'])

tpc_h.add_node('customer', attrs=[('custkey', 'integer', 'PRIMARY KEY'), 
                                  ('name', 'character varying', 'Constraint_Not_Specified'), 
                                  ('address', 'character varying', 'Constraint_Not_Specified'), 
                                  ('nationkey', 'integer', 'FOREIGN KEY')], pks=['custkey'])

tpc_h.add_node('orders', attrs=[('orderkey', 'integer', 'PRIMARY KEY'), 
                                ('custkey', 'integer', 'FOREIGN KEY'), 
                                ('status', 'character varying', 'Constraint_Not_Specified'), 
                                ('totalprice', 'integer', 'Constraint_Not_Specified')], pks=['orderkey'])

tpc_h.add_node('lineitem', attrs=[('orderkey', 'integer', 'FOREIGN KEY'), 
                                  ('partkey', 'integer', 'FOREIGN KEY'), 
                                  ('supkey', 'integer', 'FOREIGN KEY'), 
                                  ('linenumber', 'integer', 'PRIMARY KEY'), 
                                  ('status', 'character varying', 'Constraint_Not_Specified'), 
                                  ('qty', 'integer', 'Constraint_Not_Specified')], pks=['linenumber'])

tpc_h.add_node('nation', attrs=[('nationkey', 'integer', 'PRIMARY KEY'), 
                                ('name', 'character varying', 'Constraint_Not_Specified'), 
                                ('regionkey', 'integer', 'FOREIGN KEY'), 
                                ('comment', 'character varying', 'Constraint_Not_Specified')], pks=['nationkey'])

tpc_h.add_node('region', attrs=[('regionkey', 'integer', 'PRIMARY KEY'), 
                                ('name', 'character varying', 'Constraint_Not_Specified'), 
                                ('comment', 'character varying', 'Constraint_Not_Specified')], pks=['regionkey'])

edges = [
    ('lineitem', 'part', {'conditions': [('partkey', 'partkey')], 'weight':1}),
    ('lineitem', 'supplier', {'conditions': [('supkey', 'supkey')], 'weight':1}),
    ('lineitem', 'orders', {'conditions':[('orderkey', 'orderkey')], 'weight':1}),
    ('partsupp', 'part', {'conditions': [('partkey', 'partkey')], 'weight':1}),
    ('partsupp', 'supplier', {'conditions': [('supkey', 'supkey')], 'weight':1}),
    ('supplier', 'nation', {'conditions': [('nationkey', 'nationkey')], 'weight':1}),
    ('nation', 'region', {'conditions': [('regionkey', 'regionkey')], 'weight':1}),
    ('orders', 'customer', {'conditions': [('custkey', 'custkey')], 'weight':1}),
    ('customer', 'nation', {'conditions': [('nationkey', 'nationkey')], 'weight':1})
]

tpc_h.add_edges_from(edges)

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
                for attr_properties in self.db_dict[table]['attributes']:
                    attrs.append(attr_properties[0])
                    attrs.append(attr_properties[1])
                    if len(attr_properties) == 3:
                        attrs.append(attr_properties[2])
                    else:
                        attrs.append('Constraint_Not_Specified')

                query = """MERGE (:Table {name:$table, attributes: $attr_list})"""
                session.run(query, parameters={'table':table, 'attr_list': attrs})
                
            for table in self.db_dict.keys():
                for fk, ref_table, ref_attr in self.db_dict[table]['relations']:
                    query = """MATCH (t1:Table {name:$t1_name}), (t2:Table {name:$t2_name})
                               MERGE (t1) -[:HAS_FK_TO {foreign_key:$fk, referenced_attr:$ra}]-> (t2)"""
                    session.run(query, parameters={'fk':fk, 'ra': ref_attr, 't1_name': table, 't2_name': ref_table})
            
            session.close()

        driver.close()


    def get_join_graph(self):
        # driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        # try:
        #     driver.verify_connectivity()
        #     logger.info('Connection with Data Catalog succefully')
        # except Exception as e:
        #     logger.error(e)

        # join_graph = DiGraph()
        # query = """MATCH (t1:Table) RETURN t1"""
        # tables,_,_ = driver.execute_query(query,database_='neo4j')

        # #Graph Nodes
        # for table in tables:
        #     atributes = []
        #     pks = []
        #     for i in range(0, len(table['t1']['attributes']), 3):
        #         temp = []
        #         for j in range(i, i+3):
        #             temp.append(table['t1']['attributes'][j])
        #         atributes.append(tuple(temp))
        #         if 'PRIMARY KEY' in temp or 'PK FK' in temp:
        #             pks.append(temp[0])

        #     join_graph.add_node(table['t1']['name'], attrs = atributes, pks = pks)

        # #Graph Edges
        # query = """MATCH (t1:Table) -[r:HAS_FK_TO]-> (t2:Table) RETURN t1.name, r, t2.name"""
        # edges,_,_ = driver.execute_query(query, database_='neo4j')

        # for edge in edges:
        #     t1 = edge[0]
        #     t2 = edge[2]
        #     if join_graph.has_edge(t1, t2):
        #         join_graph.edges[t1, t2]['conditions'].append((edge['r']['foreign_key'], edge['r']['referenced_attr']))

        #     else:
        #         join_graph.add_edge(t1, t2, 
        #                             conditions = [(edge['r']['foreign_key'], edge['r']['referenced_attr'])], 
        #                             weight = 1)

        #DEBUG TODO
        join_graph = tpc_h

        for node in join_graph.nodes:
            for pred1 in join_graph.predecessors(node):
                for pred2 in join_graph.predecessors(node):
                    if pred1 == pred2: continue
                    for join_cond in join_graph[pred1][node]['conditions']:
                        pred2_fk = None
                        for cond in join_graph[pred2][node]['conditions']:
                            if join_cond[1] == cond[1]:
                                pred2_fk = cond[0]
                                break
                        if pred2_fk in join_graph.nodes[pred2]['pks']:
                            if join_graph.has_edge(pred1, pred2):
                                join_graph[pred1][pred2]['conditions'].append((join_cond[0], pred2_fk))
                            else:
                                join_graph.add_edge(pred1, pred2, conditions=[(join_cond[0], pred2_fk)], weight = 1)

        print(join_graph.edges.data())


        
            



        
                