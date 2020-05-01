from flask import Flask , request , jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from my_functions import get_int ,conf_vlan


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db_devices.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =SQLAlchemy(app)
ma = Marshmallow(app)

#Creating Database Schema
class Devices(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    ManagementIP = db.Column(db.String(80), unique=True, nullable=False)
    vendor = db.Column(db.String(120), unique=False, nullable=False)
    platform = db.Column(db.String(120), unique=False, nullable=False)
    role = db.Column(db.String(120), unique=False, nullable=False)

    def __init__(self , name , ManagementIP ,vendor, platform , role):
        self.name = name
        self.ManagementIP = ManagementIP
        self.vendor = vendor
        self.platform = platform
        self.role = role


class DeviceSchema(ma.Schema):
    class Meta:
        fields = ('id','name','ManagementIP','vendor','platform','role')

device_schema = DeviceSchema()
devices_schema = DeviceSchema(many=True)

#Adding Device data to database
@app.route('/device' , methods=['POST'])
def add_device():
    name = request.json['name']
    ManagementIP = request.json['ManagementIP']
    vendor = request.json['vendor']
    platform = request.json['platform']
    role = request.json['role']

    new_device = Devices(name, ManagementIP, vendor, platform, role)

    db.session.add(new_device)
    db.session.commit()

    return device_schema.jsonify(new_device)

#To Get all devices
@app.route('/device' , methods=['GET'])
def get_devices():
    all_devices = Devices.query.all()
    result = devices_schema.dump(all_devices)
    return jsonify(result)

#Get one device
@app.route('/device/<id>', methods=['GET'])
def get_single_device(id):
    device = Devices.query.get(id)

    return device_schema.jsonify(device)

#Update device data
@app.route('/device/<int:id>' , methods=['PUT'])
def update_data(id):
    device_update = Devices.query.get(id)

    name = request.json['name']
    ManagementIP = request.json['ManagementIP']
    vendor = request.json['vendor']
    platform = request.json['platform']
    role = request.json['role']

    device_update.name = name
    device_update.ManagementIP = ManagementIP
    device_update.vendor = vendor
    device_update.platform = platform
    device_update.role = role

    db.session.commit()

    return device_schema.jsonify(device_update)


#Delete Device data
@app.route('/device/<int:id>' , methods=['DELETE'])
def del_device(id):
    device = Devices.query.get(id)
    db.session.delete(device)
    db.session.commit()

    return device_schema.jsonify(device)

#Get Interface info of the Device
@app.route('/device/<int:id>/interfaces' , methods=['GET'])
def get_my_interfaces(id):
    device = Devices.query.get(id)  
    device = device.ManagementIP 
    return get_int(device)

#Configure a Vlan on the device
@app.route('/device/<int:id>/vlan/<int:v>' , methods=['POST'])
def configure_vlan(id,v):
    device = Devices.query.get(id)  
    device = device.ManagementIP 
    return conf_vlan(device,v)



if __name__ == '__main__':
    app.run(debug=True,port="7080")
