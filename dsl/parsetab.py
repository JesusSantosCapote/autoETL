
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AS AVG COUNT DIM DIVIDE FACT GROUP ID LBRACE LPAREN MINUS MONTHSTR NUMBER PLUS RBRACE RPAREN SELF SUM TIMES TWODOTS WEEKDAYDimensional_Model : List_Dimensional_TablesList_Dimensional_Tables : Dimensional_Table\n       List_Attr_Def : Attr_DefList_Dimensional_Tables : List_Dimensional_Tables Dimensional_TableDimensional_Table : DIM ID LBRACE List_Attr_Def RBRACE\n                         | FACT ID LBRACE List_Attr_Def RBRACEList_Attr_Def : List_Attr_Def Attr_DefAttr_Def : Simple_Attr\n                | Compound_AttrSimple_Attr : Attr AliasCompound_Attr : Arithmetic_Attr AliasArithmetic_Attr : T XX : PLUS T X\n         | MINUS T X\n         | emptyT : F YY : TIMES F Y\n         | DIVIDE F Y\n         | emptyF : Simple_Attr\n         | NUMBER\n         | LPAREN Arithmetic_Attr RPARENAttr : Table TWODOTS ID\n            | Table TWODOTS Func LPAREN ID RPAREN\n            | Table TWODOTS SUM LPAREN ID RPAREN GROUP Table TWODOTS ID\n            | Table TWODOTS AVG LPAREN ID RPAREN GROUP Table TWODOTS ID\n            | Table TWODOTS COUNT LPAREN ID RPAREN GROUP Table TWODOTS IDTable : ID\n             | SELFFunc : WEEKDAY\n            | MONTHSTRAlias : AS ID\n             | emptyempty : '
    
_lr_action_items = {'DIM':([0,2,3,6,25,42,],[4,4,-2,-4,-5,-6,]),'FACT':([0,2,3,6,25,42,],[5,5,-2,-4,-5,-6,]),'$end':([1,2,3,6,25,42,],[0,-1,-2,-4,-5,-6,]),'ID':([4,5,9,10,12,13,14,15,16,17,19,20,22,23,24,26,27,28,29,30,31,33,34,35,36,37,38,39,40,41,43,44,51,52,53,54,55,56,57,58,59,60,61,62,63,68,72,73,74,78,79,80,81,82,83,],[7,8,11,11,11,-3,-8,-9,-34,-34,11,-34,-34,-21,11,-7,-10,43,-33,-11,44,-20,-12,11,11,-15,-16,11,11,-19,-32,-23,-22,-34,-34,-34,-34,64,65,66,67,-13,-14,-17,-18,-24,11,11,11,81,82,83,-25,-26,-27,]),'LBRACE':([7,8,],[9,10,]),'SELF':([9,10,12,13,14,15,16,17,19,20,22,23,24,26,27,29,30,33,34,35,36,37,38,39,40,41,43,44,51,52,53,54,55,60,61,62,63,68,72,73,74,81,82,83,],[21,21,21,-3,-8,-9,-34,-34,21,-34,-34,-21,21,-7,-10,-33,-11,-20,-12,21,21,-15,-16,21,21,-19,-32,-23,-22,-34,-34,-34,-34,-13,-14,-17,-18,-24,21,21,21,-25,-26,-27,]),'NUMBER':([9,10,12,13,14,15,16,17,19,20,22,23,24,26,27,29,30,33,34,35,36,37,38,39,40,41,43,44,51,52,53,54,55,60,61,62,63,68,81,82,83,],[23,23,23,-3,-8,-9,-34,-34,23,-34,-34,-21,23,-7,-10,-33,-11,-20,-12,23,23,-15,-16,23,23,-19,-32,-23,-22,-34,-34,-34,-34,-13,-14,-17,-18,-24,-25,-26,-27,]),'LPAREN':([9,10,12,13,14,15,16,17,19,20,22,23,24,26,27,29,30,33,34,35,36,37,38,39,40,41,43,44,45,46,47,48,49,50,51,52,53,54,55,60,61,62,63,68,81,82,83,],[19,19,19,-3,-8,-9,-34,-34,19,-34,-34,-21,19,-7,-10,-33,-11,-20,-12,19,19,-15,-16,19,19,-19,-32,-23,56,57,58,59,-30,-31,-22,-34,-34,-34,-34,-13,-14,-17,-18,-24,-25,-26,-27,]),'TWODOTS':([11,18,21,75,76,77,],[-28,31,-29,78,79,80,]),'RBRACE':([12,13,14,15,16,17,20,22,23,24,26,27,29,30,33,34,37,38,41,43,44,51,52,53,54,55,60,61,62,63,68,81,82,83,],[25,-3,-8,-9,-34,-34,-34,-34,-21,42,-7,-10,-33,-11,-20,-12,-15,-16,-19,-32,-23,-22,-34,-34,-34,-34,-13,-14,-17,-18,-24,-25,-26,-27,]),'TIMES':([14,16,22,23,27,29,33,43,44,51,54,55,68,81,82,83,],[-20,-34,39,-21,-10,-33,-20,-32,-23,-22,39,39,-24,-25,-26,-27,]),'DIVIDE':([14,16,22,23,27,29,33,43,44,51,54,55,68,81,82,83,],[-20,-34,40,-21,-10,-33,-20,-32,-23,-22,40,40,-24,-25,-26,-27,]),'PLUS':([14,16,20,22,23,27,29,33,38,41,43,44,51,52,53,54,55,62,63,68,81,82,83,],[-20,-34,35,-34,-21,-10,-33,-20,-16,-19,-32,-23,-22,35,35,-34,-34,-17,-18,-24,-25,-26,-27,]),'MINUS':([14,16,20,22,23,27,29,33,38,41,43,44,51,52,53,54,55,62,63,68,81,82,83,],[-20,-34,36,-34,-21,-10,-33,-20,-16,-19,-32,-23,-22,36,36,-34,-34,-17,-18,-24,-25,-26,-27,]),'AS':([14,16,17,20,22,23,27,29,33,34,37,38,41,43,44,51,52,53,54,55,60,61,62,63,68,81,82,83,],[-20,28,28,-34,-34,-21,-10,-33,-20,-12,-15,-16,-19,-32,-23,-22,-34,-34,-34,-34,-13,-14,-17,-18,-24,-25,-26,-27,]),'RPAREN':([16,20,22,23,27,29,32,33,34,37,38,41,43,44,51,52,53,54,55,60,61,62,63,64,65,66,67,68,81,82,83,],[-34,-34,-34,-21,-10,-33,51,-20,-12,-15,-16,-19,-32,-23,-22,-34,-34,-34,-34,-13,-14,-17,-18,68,69,70,71,-24,-25,-26,-27,]),'SUM':([31,],[46,]),'AVG':([31,],[47,]),'COUNT':([31,],[48,]),'WEEKDAY':([31,],[49,]),'MONTHSTR':([31,],[50,]),'GROUP':([69,70,71,],[72,73,74,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Dimensional_Model':([0,],[1,]),'List_Dimensional_Tables':([0,],[2,]),'Dimensional_Table':([0,2,],[3,6,]),'List_Attr_Def':([9,10,],[12,24,]),'Attr_Def':([9,10,12,24,],[13,13,26,26,]),'Simple_Attr':([9,10,12,19,24,35,36,39,40,],[14,14,14,33,14,33,33,33,33,]),'Compound_Attr':([9,10,12,24,],[15,15,15,15,]),'Attr':([9,10,12,19,24,35,36,39,40,],[16,16,16,16,16,16,16,16,16,]),'Arithmetic_Attr':([9,10,12,19,24,],[17,17,17,32,17,]),'Table':([9,10,12,19,24,35,36,39,40,72,73,74,],[18,18,18,18,18,18,18,18,18,75,76,77,]),'T':([9,10,12,19,24,35,36,],[20,20,20,20,20,52,53,]),'F':([9,10,12,19,24,35,36,39,40,],[22,22,22,22,22,22,22,54,55,]),'Alias':([16,17,],[27,30,]),'empty':([16,17,20,22,52,53,54,55,],[29,29,37,41,37,37,41,41,]),'X':([20,52,53,],[34,60,61,]),'Y':([22,54,55,],[38,62,63,]),'Func':([31,],[45,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Dimensional_Model","S'",1,None,None,None),
  ('Dimensional_Model -> List_Dimensional_Tables','Dimensional_Model',1,'p_Dimensional_Model','parser_rules.py',6),
  ('List_Dimensional_Tables -> Dimensional_Table','List_Dimensional_Tables',1,'p_List_First','parser_rules.py',11),
  ('List_Attr_Def -> Attr_Def','List_Attr_Def',1,'p_List_First','parser_rules.py',12),
  ('List_Dimensional_Tables -> List_Dimensional_Tables Dimensional_Table','List_Dimensional_Tables',2,'p_List_Dimensional_Tables','parser_rules.py',17),
  ('Dimensional_Table -> DIM ID LBRACE List_Attr_Def RBRACE','Dimensional_Table',5,'p_Dimensional_Table','parser_rules.py',23),
  ('Dimensional_Table -> FACT ID LBRACE List_Attr_Def RBRACE','Dimensional_Table',5,'p_Dimensional_Table','parser_rules.py',24),
  ('List_Attr_Def -> List_Attr_Def Attr_Def','List_Attr_Def',2,'p_List_Attr_Def','parser_rules.py',33),
  ('Attr_Def -> Simple_Attr','Attr_Def',1,'p_Attr_Def','parser_rules.py',39),
  ('Attr_Def -> Compound_Attr','Attr_Def',1,'p_Attr_Def','parser_rules.py',40),
  ('Simple_Attr -> Attr Alias','Simple_Attr',2,'p_Simple_Attr','parser_rules.py',45),
  ('Compound_Attr -> Arithmetic_Attr Alias','Compound_Attr',2,'p_Compound_Attr','parser_rules.py',51),
  ('Arithmetic_Attr -> T X','Arithmetic_Attr',2,'p_Arithmetic_Attr','parser_rules.py',57),
  ('X -> PLUS T X','X',3,'p_X','parser_rules.py',63),
  ('X -> MINUS T X','X',3,'p_X','parser_rules.py',64),
  ('X -> empty','X',1,'p_X','parser_rules.py',65),
  ('T -> F Y','T',2,'p_T','parser_rules.py',74),
  ('Y -> TIMES F Y','Y',3,'p_Y','parser_rules.py',79),
  ('Y -> DIVIDE F Y','Y',3,'p_Y','parser_rules.py',80),
  ('Y -> empty','Y',1,'p_Y','parser_rules.py',81),
  ('F -> Simple_Attr','F',1,'p_F','parser_rules.py',90),
  ('F -> NUMBER','F',1,'p_F','parser_rules.py',91),
  ('F -> LPAREN Arithmetic_Attr RPAREN','F',3,'p_F','parser_rules.py',92),
  ('Attr -> Table TWODOTS ID','Attr',3,'p_Attr','parser_rules.py',110),
  ('Attr -> Table TWODOTS Func LPAREN ID RPAREN','Attr',6,'p_Attr','parser_rules.py',111),
  ('Attr -> Table TWODOTS SUM LPAREN ID RPAREN GROUP Table TWODOTS ID','Attr',10,'p_Attr','parser_rules.py',112),
  ('Attr -> Table TWODOTS AVG LPAREN ID RPAREN GROUP Table TWODOTS ID','Attr',10,'p_Attr','parser_rules.py',113),
  ('Attr -> Table TWODOTS COUNT LPAREN ID RPAREN GROUP Table TWODOTS ID','Attr',10,'p_Attr','parser_rules.py',114),
  ('Table -> ID','Table',1,'p_Table','parser_rules.py',127),
  ('Table -> SELF','Table',1,'p_Table','parser_rules.py',128),
  ('Func -> WEEKDAY','Func',1,'p_Func','parser_rules.py',133),
  ('Func -> MONTHSTR','Func',1,'p_Func','parser_rules.py',134),
  ('Alias -> AS ID','Alias',2,'p_Alias','parser_rules.py',139),
  ('Alias -> empty','Alias',1,'p_Alias','parser_rules.py',140),
  ('empty -> <empty>','empty',0,'p_empty','parser_rules.py',146),
]
