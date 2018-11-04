INSERT INTO locations VALUES('CAL01', 'Calgary', 'Alberta', 'Uni Calgary');
INSERT INTO locations VALUES('CAL02', 'Calgary', 'Alberta', 'Chinook Mall');
INSERT INTO locations VALUES('CAL03', 'Calgary', 'Alberta', 'Stadium');
INSERT INTO locations VALUES('CAL04', 'Calgary', 'Alberta', 'Hospital');
INSERT INTO locations VALUES('CAL05', 'Calgary', 'Alberta', 'IKEA');
INSERT INTO locations VALUES('BAL01', 'Balzac', 'Alberta', 'Cross Iron');
INSERT INTO locations VALUES('EDM01', 'Edmonton', 'Alberta', 'Uni Alberta');
INSERT INTO locations VALUES('EDM02', 'Edmonton', 'Alberta', 'Rogers Place');
INSERT INTO locations VALUES('EDM03', 'Edmonton', 'Alberta', 'Zoo');
INSERT INTO locations VALUES('EDM04', 'Edmonton', 'Alberta', 'Muttart Conserv');
INSERT INTO locations VALUES('EDM05', 'Edmonton', 'Alberta', 'Mall');

INSERT INTO cars VALUES('1', 'Toyota', 'Matrix', '2009', '5', 'tom.maurer@yahoo.com');
INSERT INTO cars VALUES('2', 'VolksWagen', 'Golf GTI', '2013', '5', 'tom.maurer@yahoo.com');
INSERT INTO cars VALUES('3', 'Ducati', 'Monster 695', '2007', '2', 'tom.maurer@yahoo.com');
INSERT INTO cars VALUES('4', 'Toyota', 'Corolla', '2003', '5', 'coleb@hotmail.ca');
INSERT INTO cars VALUES('5', 'Honda', 'Civic', '2018', '5', 'coleb@hotmail.ca');
INSERT INTO cars VALUES('6', 'Smart', 'Car', '2016', '2', 'coleb@hotmail.ca');
INSERT INTO cars VALUES('7', 'Mini', 'Cooper S', '2012', '4', 'joPoulin@hotmail.ca');
INSERT INTO cars VALUES('8', 'Jeep', 'Wrangler', '2008', '5', 'LoganYue@gmail.com');
INSERT INTO cars VALUES('9', 'Chevrolet', 'Suburban', '2004', '7', 'syd.b@shaw.ca');

INSERT INTO members VALUES('tom.maurer@yahoo.com', 'Tom Maurer', '403-999-2662', 'PASSTM');
INSERT INTO members VALUES('coleb@hotmail.ca', 'Cole Batonyi', '403-777-2889', 'PASSCB');
INSERT INTO members VALUES('joPoulin@hotmail.ca', 'Jo Poulin', '587-264-9832', 'PASSJP');
INSERT INTO members VALUES('LoganYue@gmail.com', 'Logan Yue', '587-392-6487', 'PASSLY');
INSERT INTO members VALUES('syd.b@hotmail.ca', 'Syd Bachalo', '629-878-4351', 'PASSSB');

INSERT INTO rides VALUES('1', '5', '2018-12-10', '3', 'Small','CAL01','CAL04','tom.maurer@yahoo.com','1');
INSERT INTO rides VALUES('2', '20', '2018-12-20', '4', 'Small','EDM01','CAL01','tom.maurer@yahoo.com','2');
INSERT INTO rides VALUES('3', '14', '2019-07-13', '1', 'Big','CAL01','BAL01','coleb@hotmail.ca','4');
INSERT INTO rides VALUES('4', '3', '2019-01-01', '2', 'Big','CAL01','CAL02','joPoulin@hotmail.ca','');

INSERT INTO enroute VALUES('1', 'CAL02');
INSERT INTO enroute VALUES('1', 'CAL03');
INSERT INTO enroute VALUES('2', 'BAL01');
