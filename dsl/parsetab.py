
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AS AVG COUNT DIM DIVIDE FACT GROUP ID LBRACE LPAREN MINUS MONTHSTR NUMBER PLUS RBRACE RPAREN SELF SUM TIMES TWODOTS WEEKDAYDimensional_Model : List_Dimensional_TablesList_Dimensional_Tables : Dimensional_Table\n       List_Attr_Def : Attr_DefList_Dimensional_Tables : List_Dimensional_Tables Dimensional_TableDimensional_Table : DIM ID LBRACE List_Attr_Def RBRACE\n                         | FACT ID LBRACE List_Attr_Def RBRACEList_Attr_Def : List_Attr_Def Attr_DefAttr_Def : Attr_Expression AliasAttr_Expression : T XX : PLUS T X\n         | MINUS T X\n         | empty_listT : F YY : TIMES F Y\n         | DIVIDE F Y\n         | empty_listF : Attr\n         | NUMBER\n         | LPAREN Attr_Expression RPARENAttr : Table TWODOTS ID\n            | Table TWODOTS Func LPAREN ID RPAREN\n            | Table TWODOTS SUM LPAREN ID RPAREN GROUP Table TWODOTS ID\n            | Table TWODOTS AVG LPAREN ID RPAREN GROUP Table TWODOTS ID\n            | Table TWODOTS COUNT LPAREN ID RPAREN GROUP Table TWODOTS IDTable : ID\n             | SELFFunc : WEEKDAY\n            | MONTHSTRAlias : AS ID\n             | emptyempty : empty_list : '
    
_lr_action_items = {'DIM':([0,2,3,6,23,38,],[4,4,-2,-4,-5,-6,]),'FACT':([0,2,3,6,23,38,],[5,5,-2,-4,-5,-6,]),'$end':([1,2,3,6,23,38,],[0,-1,-2,-4,-5,-6,]),'ID':([4,5,9,10,12,13,14,15,16,17,18,19,22,24,25,26,27,28,29,30,31,32,33,34,35,37,39,40,41,42,43,44,45,52,53,54,55,56,57,58,59,64,68,69,70,74,75,76,77,78,79,],[7,8,11,11,11,-3,-31,-32,-32,-17,-18,11,11,-7,-8,39,-30,-9,11,11,-12,-13,11,11,-16,45,-29,-32,-32,-32,-32,-19,-20,-10,-11,-14,-15,60,61,62,63,-21,11,11,11,77,78,79,-22,-23,-24,]),'LBRACE':([7,8,],[9,10,]),'NUMBER':([9,10,12,13,14,15,16,17,18,19,22,24,25,27,28,29,30,31,32,33,34,35,39,40,41,42,43,44,45,52,53,54,55,64,77,78,79,],[18,18,18,-3,-31,-32,-32,-17,-18,18,18,-7,-8,-30,-9,18,18,-12,-13,18,18,-16,-29,-32,-32,-32,-32,-19,-20,-10,-11,-14,-15,-21,-22,-23,-24,]),'LPAREN':([9,10,12,13,14,15,16,17,18,19,22,24,25,27,28,29,30,31,32,33,34,35,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,64,77,78,79,],[19,19,19,-3,-31,-32,-32,-17,-18,19,19,-7,-8,-30,-9,19,19,-12,-13,19,19,-16,-29,-32,-32,-32,-32,-19,-20,56,57,58,59,-27,-28,-10,-11,-14,-15,-21,-22,-23,-24,]),'SELF':([9,10,12,13,14,15,16,17,18,19,22,24,25,27,28,29,30,31,32,33,34,35,39,40,41,42,43,44,45,52,53,54,55,64,68,69,70,77,78,79,],[21,21,21,-3,-31,-32,-32,-17,-18,21,21,-7,-8,-30,-9,21,21,-12,-13,21,21,-16,-29,-32,-32,-32,-32,-19,-20,-10,-11,-14,-15,-21,21,21,21,-22,-23,-24,]),'TWODOTS':([11,20,21,71,72,73,],[-25,37,-26,74,75,76,]),'RBRACE':([12,13,14,15,16,17,18,22,24,25,27,28,31,32,35,39,40,41,42,43,44,45,52,53,54,55,64,77,78,79,],[23,-3,-31,-32,-32,-17,-18,38,-7,-8,-30,-9,-12,-13,-16,-29,-32,-32,-32,-32,-19,-20,-10,-11,-14,-15,-21,-22,-23,-24,]),'AS':([14,15,16,17,18,28,31,32,35,40,41,42,43,44,45,52,53,54,55,64,77,78,79,],[26,-32,-32,-17,-18,-9,-12,-13,-16,-32,-32,-32,-32,-19,-20,-10,-11,-14,-15,-21,-22,-23,-24,]),'PLUS':([15,16,17,18,32,35,40,41,42,43,44,45,54,55,64,77,78,79,],[29,-32,-17,-18,-13,-16,29,29,-32,-32,-19,-20,-14,-15,-21,-22,-23,-24,]),'MINUS':([15,16,17,18,32,35,40,41,42,43,44,45,54,55,64,77,78,79,],[30,-32,-17,-18,-13,-16,30,30,-32,-32,-19,-20,-14,-15,-21,-22,-23,-24,]),'RPAREN':([15,16,17,18,28,31,32,35,36,40,41,42,43,44,45,52,53,54,55,60,61,62,63,64,77,78,79,],[-32,-32,-17,-18,-9,-12,-13,-16,44,-32,-32,-32,-32,-19,-20,-10,-11,-14,-15,64,65,66,67,-21,-22,-23,-24,]),'TIMES':([16,17,18,42,43,44,45,64,77,78,79,],[33,-17,-18,33,33,-19,-20,-21,-22,-23,-24,]),'DIVIDE':([16,17,18,42,43,44,45,64,77,78,79,],[34,-17,-18,34,34,-19,-20,-21,-22,-23,-24,]),'SUM':([37,],[47,]),'AVG':([37,],[48,]),'COUNT':([37,],[49,]),'WEEKDAY':([37,],[50,]),'MONTHSTR':([37,],[51,]),'GROUP':([65,66,67,],[68,69,70,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Dimensional_Model':([0,],[1,]),'List_Dimensional_Tables':([0,],[2,]),'Dimensional_Table':([0,2,],[3,6,]),'List_Attr_Def':([9,10,],[12,22,]),'Attr_Def':([9,10,12,22,],[13,13,24,24,]),'Attr_Expression':([9,10,12,19,22,],[14,14,14,36,14,]),'T':([9,10,12,19,22,29,30,],[15,15,15,15,15,40,41,]),'F':([9,10,12,19,22,29,30,33,34,],[16,16,16,16,16,16,16,42,43,]),'Attr':([9,10,12,19,22,29,30,33,34,],[17,17,17,17,17,17,17,17,17,]),'Table':([9,10,12,19,22,29,30,33,34,68,69,70,],[20,20,20,20,20,20,20,20,20,71,72,73,]),'Alias':([14,],[25,]),'empty':([14,],[27,]),'X':([15,40,41,],[28,52,53,]),'empty_list':([15,16,40,41,42,43,],[31,35,31,31,35,35,]),'Y':([16,42,43,],[32,54,55,]),'Func':([37,],[46,]),}

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
  ('Attr_Def -> Attr_Expression Alias','Attr_Def',2,'p_Attr_Def','parser_rules.py',39),
  ('Attr_Expression -> T X','Attr_Expression',2,'p_Attr_Expression','parser_rules.py',45),
  ('X -> PLUS T X','X',3,'p_X','parser_rules.py',50),
  ('X -> MINUS T X','X',3,'p_X','parser_rules.py',51),
  ('X -> empty_list','X',1,'p_X','parser_rules.py',52),
  ('T -> F Y','T',2,'p_T','parser_rules.py',61),
  ('Y -> TIMES F Y','Y',3,'p_Y','parser_rules.py',66),
  ('Y -> DIVIDE F Y','Y',3,'p_Y','parser_rules.py',67),
  ('Y -> empty_list','Y',1,'p_Y','parser_rules.py',68),
  ('F -> Attr','F',1,'p_F','parser_rules.py',77),
  ('F -> NUMBER','F',1,'p_F','parser_rules.py',78),
  ('F -> LPAREN Attr_Expression RPAREN','F',3,'p_F','parser_rules.py',79),
  ('Attr -> Table TWODOTS ID','Attr',3,'p_Attr','parser_rules.py',93),
  ('Attr -> Table TWODOTS Func LPAREN ID RPAREN','Attr',6,'p_Attr','parser_rules.py',94),
  ('Attr -> Table TWODOTS SUM LPAREN ID RPAREN GROUP Table TWODOTS ID','Attr',10,'p_Attr','parser_rules.py',95),
  ('Attr -> Table TWODOTS AVG LPAREN ID RPAREN GROUP Table TWODOTS ID','Attr',10,'p_Attr','parser_rules.py',96),
  ('Attr -> Table TWODOTS COUNT LPAREN ID RPAREN GROUP Table TWODOTS ID','Attr',10,'p_Attr','parser_rules.py',97),
  ('Table -> ID','Table',1,'p_Table','parser_rules.py',110),
  ('Table -> SELF','Table',1,'p_Table','parser_rules.py',111),
  ('Func -> WEEKDAY','Func',1,'p_Func','parser_rules.py',116),
  ('Func -> MONTHSTR','Func',1,'p_Func','parser_rules.py',117),
  ('Alias -> AS ID','Alias',2,'p_Alias','parser_rules.py',122),
  ('Alias -> empty','Alias',1,'p_Alias','parser_rules.py',123),
  ('empty -> <empty>','empty',0,'p_empty','parser_rules.py',129),
  ('empty_list -> <empty>','empty_list',0,'p_empty_list','parser_rules.py',134),
]
