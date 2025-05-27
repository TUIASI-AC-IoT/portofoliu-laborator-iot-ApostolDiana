from flask import Flask
from flask import jsonify
from flask import request, abort, make_response
app = Flask(__name__)

directory=[
    {
        'name':'file1',
        'content':'abcd efgh'
    },
    {
        'name':'file2',
        'content':'ijkl mnop'
    },
    {
        'name':'file3',
        'content':'qrst wxyz'
    },
    {
        'name':'file4',
        'content':'1234 5678'
    }
]

#hateoas
def add_file_links(file):
    return {
        **file,
        '_links': {
            'self': f'/directory/files/{file["name"]}',
            'update': {
                'href': f'/directory/files/{file["name"]}',
                'method': 'PUT'
            },
            'delete': {
                'href': f'/directory/files/{file["name"]}',
                'method': 'DELETE'
            },
            'parent': {
                'href': '/directory/files',
                'method': 'GET'
            }
        }
    }


def add_directory_links(files):
    return {
        'Files': [add_file_links(file) for file in files],
        '_links': {
            'self': {
                'href': '/directory/files',
                'method': 'GET'
            },
            'create': {
                'href': '/directory/files',
                'method': 'POST'
            }
        }
    }

# listarea continutului directorului => 'GET'
@app.route('/directory/files',methods=['GET'])
def getAllFiles():
    return jsonify(add_directory_links(directory)), 200

# listarea continutului unui fisier text specificat prin nume => 'GET'
@app.route('/directory/files/<name>',methods=['GET'])
def getFile(name):
    file = next((file for file in directory if (file['name'] == name)), None)
    if file is None:
        abort(404, description="NOT FOUND")
    return jsonify({'File': add_file_links(file)}), 200

   

# crearea unui fisier specificat prin nume si continut => 'PUT'
# modificarea continutului unui fisier specificat prin nume =>'PUT'
@app.route('/directory/files/<name>',methods=['PUT'])
def updateOrCreateFile(name):
    if not request.is_json:
        abort(400, description="BAD REQUEST")

    file = [ file for file in directory if (file['name'] == name) ]
    
    if not file:
        data = {
            'name':request.json['name'],
            'content':request.json['content']
            }
        directory.append(data)
        return jsonify(data), 201
    else:
        if 'name' in request.json : 
            file[0]['name'] = request.json['name']

        if 'content' in request.json:
            file[0]['content'] = request.json['content']

        return jsonify({'File': add_file_links(file[0])}), 200
    
# crearea unui fisier specificat prin continut => POST
@app.route('/directory/files',methods=['POST'])
def createFile():
    if not request.is_json:
        abort(400, description="BAD REQUEST")
        
    name = "file" + str(len(directory) + 1)

    data = {
    'name': name,
    'content':request.json['content']
    }
    directory.append(data)
    return jsonify(add_file_links(data)), 201

# stergerea unui fisier specificat prin nume => DELETE
@app.route('/directory/files/<name>',methods=['DELETE'])
def deleteFile(name):
    file = next(( file for file in directory if (file['name'] == name)), None)
    
    if file is None:
        abort(404, description="NOT FOUND")

    directory.remove(file)
    return '', 204


if __name__ == "__main__":
    app.run()