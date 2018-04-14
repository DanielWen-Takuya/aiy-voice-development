INSERT INTO auth_role VALUES (DEFAULT,'admin','Administration role that can control all');
INSERT INTO auth_role VALUES (DEFAULT,'collab','Collaborator role that can modify partial tables');
INSERT INTO auth_role VALUES (DEFAULT,'visitor','Visitor role that can only view the data');

INSERT INTO auth_user VALUES (DEFAULT,'Zoutao','Wen','for change',TRUE,'daniel27wen@gmail.com','Creator of the AIY database');

INSERT INTO auth_user_role VALUES ('1','1',now(),'infinity'::timestamp);
