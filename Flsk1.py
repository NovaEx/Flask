from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_marshmallow import Marshmallow


#Database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp/flasksql.db'

# Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)


class Dept(db.Model):
    deptno = db.Column(db.Integer, primary_key=True)
    dname = db.Column(db.String)
    loc = db.Column(db.String)

    def __init__(self, dname, loc):
        self.dname = dname
        self.loc = loc


class DeptSchema(ma.Schema):
    class Meta:
        fields = ('deptno', 'dname', 'loc')


class Emp(db.Model):
    empno = db.Column(db.Integer, primary_key=True, unique=True)
    ename = db.Column(db.String)
    job = db.Column(db.String)
    mgr = db.Column(db.Integer)
    hiredate = db.Column(db.Integer)
    sal = db.Column(db.Integer)
    comm = db.Column(db.Integer)
    deptno = db.Column(db.ForeignKey("dept.deptno"))

    def __init__(self, ename, job, mgr, hiredate, sal, comm, deptno):
        self.ename = ename
        self.job = job
        self.mgr = mgr
        self.hiredate = hiredate
        self.sal = sal
        self.comm = comm
        self.deptno = deptno


class EmpSchema(ma.Schema):
    class Meta:
        fields = ('empno', 'ename', 'job', 'mgr', 'hiredate', 'sal', 'comm', 'deptno')


class Salgrade(db.Model):
    grade = db.Column(db.Integer, primary_key=True)
    losal = db.Column(db.Integer)
    hisal = db.Column(db.Integer)

    def __init__(self, losal, hisal):
        self.losal = losal
        self.hisal = hisal


class SalgradeSchema(ma.Schema):
    class Meta:
        fields = ('grade', 'losal', 'hisal')


dept_schema = DeptSchema(strict=True)
depts_schema = DeptSchema(many=True, strict=True)
emp_schema = EmpSchema(strict=True)
emps_schema = EmpSchema(many=True, strict=True)
salgrade_schema = SalgradeSchema(strict=True)
salgrades_schema  = SalgradeSchema(many=True, strict=True)


def allget(whs):
    return whs.query.all()


# OPERATIONS DEPT
@app.route('/dept', methods=['GET'])
def get_depts():
    result = depts_schema.dump(allget(Dept))
    return jsonify(result.data)

@app.route('/dept/<deptno>', methods=['GET'])
def get_deptno(deptno):
    dept = Dept.query.get(deptno)
    if dept is None: return jsonify({'msg': 'This deptno not found.'})
    return dept_schema.jsonify(dept)

@app.route('/dept', methods=['POST'])
def add_dept():
    dname = request.json['dname']
    loc = request.json['loc']
    new_dept = Dept(dname, loc)
    db.session.add(new_dept)
    db.session.commit()
    return dept_schema.jsonify(new_dept)

@app.route('/dept/<deptno>', methods=['PUT'])
def upd_dept(deptno):
    dept = Dept.query.get(deptno)
    dname = request.json['dname']
    loc = request.json['loc']

    dept.dname = dname
    dept.loc = loc

    db.session.commit()
    return dept_schema.jsonify(dept)

@app.route('/dept/<deptno>', methods=['DELETE'])
def del_dept(deptno):
    dept = Dept.query.get(deptno)
    db.session.delete(dept)
    db.session.commit()
    return dept_schema.jsonify(dept)



# OPERATIONS EMP
@app.route('/emp', methods=['GET'])
def get_emps():
    result = emps_schema.dump(allget(Emp))
    return jsonify(result.data)

@app.route('/emp/<empno>', methods=['GET'])
def get_emp(empno):
    emp = Emp.query.get(empno)
    if emp is None: return jsonify({'msg': 'This emp not found.'})
    return emp_schema.jsonify(emp)

@app.route('/emp', methods=['POST'])
def add_emp():
    ename = request.json['ename']
    job = request.json['job']
    mgr = request.json['mgr']
    hiredate = request.json['hiredate']
    sal = request.json['sal']
    comm = request.json['comm']
    deptno = request.json['deptno']
    new_emp = Emp(ename, job, mgr, hiredate, sal, comm, deptno)
    db.session.add(new_emp)
    db.session.commit()
    return emp_schema.jsonify(new_emp)

@app.route('/emp/<empno>', methods=['PUT'])
def upd_emp(empno):
    emp = Dept.query.get(empno)
    ename = request.json['ename']
    job = request.json['job']
    mgr = request.json['mgr']
    hiredate = request.json['hiredate']
    sal = request.json['sal']
    comm = request.json['comm']
    deptno = request.json['deptno']

    emp.ename = ename
    emp.loc = job
    emp.mgr = mgr
    emp.hiredate = hiredate
    emp.sal = sal
    emp.comm = comm
    emp.deptno =deptno

    db.session.commit()
    return emp_schema.jsonify(emp)

@app.route('/emp/<empno>', methods=['DELETE'])
def del_emp(empno):
    emp = Emp.query.get(empno)
    db.session.delete(emp)
    db.session.commit()
    return emp_schema.jsonify(emp)



# OPERATIONS GRADE
@app.route('/grade', methods=['GET'])
def get_grades():
    result = salgrades_schema.dump(allget(Salgrade))
    return jsonify(result.data)

@app.route('/grade/<grade>', methods=['GET'])
def get_grade(grade):
    grd = Salgrade.query.get(grade)
    if grd is None: return jsonify({'msg': 'This grade doesn\'t exist.'})
    return salgrade_schema.jsonify(grd)

@app.route('/grade', methods=['POST'])
def add_grade():
    losal = request.json['losal']
    hisal = request.json['hisal']
    new_grade = Salgrade(losal, hisal)
    db.session.add(new_grade)
    db.session.commit()
    return salgrade_schema.jsonify(new_grade)

@app.route('/dept/<grade>', methods=['PUT'])
def upd_grade(grade_id):
    grade = Dept.query.get(grade_id)
    name = request.json['losal']
    hisal = request.json['hisal']

    grade.name = name
    grade.hisal = hisal

    db.session.commit()
    return salgrade_schema.jsonify(grade)

@app.route('/grade/<grade>', methods=['DELETE'])
def del_grade(grade):
    sgrade = Salgrade.query.get(grade)
    db.session.delete(sgrade)
    db.session.commit()
    return salgrade_schema.jsonify(sgrade)



if __name__ == '__main__':
    app.run(debug=True)

