from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/insertuser', methods=['POST'])
def insert_user():
    try:
        # Parse request data
        data = request.json
        id = data['id']
        username = data['utilizator']
        password = data['parola']
        email = data['mail']

        # Insert data into database using psycopg2
        conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
        cur = conn.cursor()
        cur.execute("INSERT INTO utilizator(id, username, password, email) VALUES (%s,%s,%s,%s)",(id, username, password, email))
        conn.commit()
        conn.close()

        # Return success response
        return jsonify({'success': True}), 200

    except Exception as e:
        # Log the error message
        print(str(e))

        # Return error response with detailed message
        return jsonify({'error': str(e)}), 500
@app.route('/maxid', methods=['GET'])
def get_max_id():
    try:
        conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
        cur = conn.cursor()
        cur.execute("SELECT MAX(id) FROM utilizator;")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({'max_id': result}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    # obținem datele din cerere
    data = request.get_json()
    email = data['email']
    password = data['password']

    # căutăm utilizatorul în baza de date
    conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
    cur = conn.cursor()
    cur.execute("SELECT id FROM utilizator WHERE email = %s AND password = %s;", (email, password))
    user_id = cur.fetchone()
    conn.close()

    # verificăm dacă utilizatorul a fost găsit
    if user_id is not None:
        # returnăm un răspuns de succes
        return jsonify({'status': 'success', 'user_id': user_id[0]}), 200
    else:
        # returnăm un răspuns de eroare
        return jsonify({'status': 'error', 'message': 'Email sau parolă incorectă!'}), 401


@app.route('/adaugaanunturi', methods=['POST'])
def adauga_anunt():
    # obținem datele din cerere
    data = request.get_json()
    id_user = data['id_user']
    imagine = data['imagine']
    titlu = data['titlu']
    descriere = data['descriere']
    rating = data['rating']
    pret = data['pret']
    adresa = data['adresa']
    domeniu = data['domeniu']
    judet = data['judet']
    oras = data['oras']

    # adăugăm anunțul în baza de date
    conn = psycopg2.connect(
        "dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
    cur = conn.cursor()
    cur.execute("INSERT INTO anunturi (id_user, imagine, titlu, descriere, rating, pret, adresa, domeniu, judet, oras) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(id_user, imagine, titlu, descriere, rating, pret, adresa, domeniu, judet, oras))
    conn.commit()
    conn.close()

    # returnăm un răspuns de succes
    return jsonify({'status': 'success', 'message': 'Anuntul a fost adaugat cu succes!'}), 201

@app.route('/insertsuplimentar', methods=['POST'])
def insert_suplimentar():
    try:
        # Parse request data
        data = request.json
        iduser = data['iduser']
        poza = data['poza']
        adresa = data['adresa']
        telefon = data['telefon']
        judet = data['judet']
        oras = data['oras']
        # Insert data into database using psycopg2
        conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
        cur = conn.cursor()
        cur.execute("INSERT INTO informatiisuplimentare (iduser, poza, adresa, telefon, judet, oras) VALUES (%s, %s, %s, %s, %s, %s );",(iduser, poza, adresa, telefon, judet,oras))
        conn.commit()
        conn.close()

        # Return success response
        return jsonify({'success': True}), 200

    except Exception as e:
        # Log the error message
        print(str(e))

        # Return error response with detailed message
        return jsonify({'error': str(e)}), 500

@app.route('/selectnume', methods=['GET'])
def get_nume():
    try:
        iduser = request.args.get('iduser')
        conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
        cur = conn.cursor()
        cur.execute("Select username from utilizator where id = %s",(iduser))
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"result": result}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/selectinformatii', methods=['GET'])
def get_informatiisuplimentare():
    try:
        iduser = request.args.get('iduser')
        conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
        cur = conn.cursor()
        cur.execute("SELECT * FROM informatiisuplimentare WHERE iduser=%s",(iduser))
        results = cur.fetchall()
        cur.close()
        conn.close()
        if results is not None:
            return jsonify({"result": results}), 200
        else:
            return jsonify({"result": []}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/insertrating', methods=['POST'])
def insert_rating():
    try:
        # Parse request data
        data = request.json
        iduser = data['iduser']
        idanunt = data['idanunt']
        nota = data['nota']

        # Check if rating already exists
        conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
        cur = conn.cursor()
        cur.execute("select count(*) from rating where iduser=%s and idanunt=%s;", (iduser, idanunt))
        count = cur.fetchone()[0]
        cur.close()

        if count == 0:
            # Insert data into database using psycopg2
            conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
            cur = conn.cursor()
            cur.execute("insert into rating (iduser, idanunt, nota) values (%s,%s,%s);",(iduser, idanunt, nota))
            conn.commit()
            conn.close()

            # Return success response
            return jsonify({'success': True}), 200
        else:
            # Return error response with detailed message
            error_msg = "Rating already exists for user {} and ad {}.".format(iduser, idanunt)
            return jsonify({'error': error_msg}), 400

    except Exception as e:
        # Log the error message
        print(str(e))

        # Return error response with detailed message
        return jsonify({'error': str(e)}), 500

@app.route('/anuleazarating', methods=['POST'])
def anuleazarating():
    try:
        # Parse request data
        data = request.json
        iduser = data['iduser']
        idanunt = data['idanunt']
        # Insert data into database using psycopg2
        conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
        cur = conn.cursor()
        cur.execute("delete from rating where iduser = %s and idanunt = %s;",(iduser, idanunt))
        conn.commit()
        conn.close()

        # Return success response
        return jsonify({'success': True}), 200

    except Exception as e:
        # Log the error message
        print(str(e))

        # Return error response with detailed message
        return jsonify({'error': str(e)}), 500

@app.route('/cauta', methods=['POST'])
def cauta():
    try:
        # Parse request data
        data = request.json
        oras = data.get('oras')
        domeniu = data.get('domeniu')
        cuvant_cheie = data.get('cuvant_cheie')
        pret = data.get('pret')

        # Build SQL query based on filters
        query = """
            SELECT * FROM anunturi 
            WHERE 
                (oras = %s OR %s IS NULL) 
                AND (domeniu = %s OR %s IS NULL) 
                AND ((titlu LIKE %s OR titlu LIKE %s OR titlu LIKE %s) OR %s IS NULL) 
                AND (pret = %s OR %s IS NULL);
        """

        # Connect to database using psycopg2
        conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
        cur = conn.cursor()

        # Execute query with parameters and fetch results
        if cuvant_cheie is None:
            cur.execute(query, (oras, oras, domeniu, domeniu, None, None, None, None, pret, pret))
        else:
            cur.execute(query, (oras, oras, domeniu, domeniu, '%' + cuvant_cheie, '%' + cuvant_cheie + '%', cuvant_cheie + '%', cuvant_cheie, pret, pret))

        results = cur.fetchall()

        # Close database connection
        conn.close()

        # Return success response with results
        return jsonify({'results': results}), 200

    except Exception as e:
        # Log the error message
        print(str(e))

        # Return error response with detailed message
        return jsonify({'error': str(e)}), 500

@app.route('/stergeanunturi', methods=['POST'])
def sterge_anunt():
    # obținem datele din cerere
    data = request.get_json()
    id = data['id']
    id_user = data['id_user']


    # adăugăm anunțul în baza de date
    conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
    cur = conn.cursor()
    cur.execute("DELETE FROM anunturi WHERE id = %s AND id_user = %s;",(id,id_user))
    conn.commit()
    conn.close()

    # returnăm un răspuns de succes
    return jsonify({'status': 'success', 'message': 'Anuntul a fost sters cu succes!'}), 201

@app.route('/actualizareinformatiisuplimentare', methods=['POST'])
def actualizareinformatiisuplimentare():
    # obținem datele din cerere
    data = request.get_json()
    iduser = data['iduser']
    poza = data['poza']
    adresa = data['adresa']
    telefon = data['telefon']
    judet = data['judet']
    oras = data['oras']


    # adăugăm anunțul în baza de date
    conn = psycopg2.connect("dbname='licenta' user='postgres' password='parolaaa' port='5432' host='licenta.cqpg37vykvyw.us-east-2.rds.amazonaws.com'")
    cur = conn.cursor()
    cur.execute("update informatiisuplimentare set poza = %s, adresa=%s, telefon=%s, judet=%s, oras=%s where iduser = %s",( poza, adresa, telefon, judet,oras, iduser))
    conn.commit()
    conn.close()

    # returnăm un răspuns de succes
    return jsonify({'status': 'success', 'message': 'Informatii suplimentare actualizate!'}), 201

if __name__ == '__main__':
    app.run(debug=True)