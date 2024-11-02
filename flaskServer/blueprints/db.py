from asyncio.windows_events import NULL
import sqlite3

DB_FILENAME = "db.db"


def connect():
    try: 
        db_connection = sqlite3.connect(DB_FILENAME)
        db_cursor = db_connection.cursor()
        print("DB successfully connected")
        return db_cursor
    
    except sqlite3.Error:
        print("Error: DB connection Error: ", sqlite3.Error)
        
def disconnect(db_cursor):
    db_cursor.close()
    db_cursor.connection.commit()
    db_cursor.connection.close()
    


def get_user_by_mail(email):
    db_cursor = connect()
    sqlite_query = "SELECT * FROM users WHERE mail_adress = ?"
    db_cursor.execute(sqlite_query, (email,))
    
    record = db_cursor.fetchone()
    disconnect(db_cursor)
    return record

def check_if_mail_is_available(email):
    db_cursor = connect()
    sqlite_query = "SELECT * FROM users WHERE mail_adress = (?)"
    db_cursor.execute(sqlite_query, (email,))
    
    record = db_cursor.fetchone()
    disconnect(db_cursor)
    
    if record is None:
        #No Records of the email -> email is available
        return True
    else:
        return False

#Add User to db and returns its user id
def add_user(municipalitie, fire_station, first_name, last_name, email, hashed_password, rank = 0):
    db_cursor = connect()
    sqlite_query = "INSERT INTO users (first_name, last_name, mail_adress, password, rank) VALUES (?, ?, ?, ?, ?)"
    db_cursor.execute(sqlite_query, (first_name, last_name, email, hashed_password, rank))
    
    user_id = db_cursor.lastrowid
    
    disconnect(db_cursor)
    return user_id

def add_user_qualifications(user_id):
    db_cursor = connect()
    sqlite_query = """
    SELECT 
    qualification_id
    FROM qualifications
    """
    db_cursor.execute(sqlite_query)
    data = db_cursor.fetchall()
    disconnect(db_cursor)
    
    
    insert_template = """
    INSERT INTO 
    user_qualifications (user_id, qualification_id, sessions_done, is_done)
    VALUES
    (?,?,0,0)
    """
    insert_values = []
    
    for row in data:
        insert_values.append((user_id, row[0]))
    
    if insert_values:
        db_cursor = connect()
        db_cursor.executemany(insert_template, insert_values)
        disconnect(db_cursor)
    
    return

def get_user_name(user_id):
    db_cursor = connect()
    sqlite_query = """
    SELECT 
    first_name, last_name
    FROM users
    WHERE
    user_id = (?)
    """
    db_cursor.execute(sqlite_query, (user_id, ))
    data = db_cursor.fetchone()
    disconnect(db_cursor)
    return data

def update_user_sessions_done(user_id, qualification_id, amount):
    db_cursor = connect()
    sqlite_query = """
    UPDATE
    user_qualifications
    SET amount_sessions_completed = amount_sessions_completed + (?)
    WHERE
    user_qualifications.user_id = (?)
    AND
    user_qualifications.qualification_id = (?)
    """
    db_cursor.execute(sqlite_query, (amount, user_id, qualification_id))
    disconnect(db_cursor)


def add_sessions(qualification_id, user_id):
    #Get needed session for qualification
    db_cursor = connect()
    sqlite_query = """
    SELECT
    training_units.training_unit_id, training_units.theory_sessions, training_units.practical_sessions, training_units.additional_sessions
    FROM 
    training_units
    INNER JOIN 
    qualifications_training_units
    ON
    qualifications_training_units.training_unit_id = training_units.training_unit_id
    WHERE
    qualifications_training_units.qualification_id = (?)
    """
    db_cursor.execute(sqlite_query, (qualification_id,))
    data = db_cursor.fetchall()
    
    disconnect(db_cursor)
    
    
    #Add sessions to user_sessions
    sqlite_query = ""
    
    insert_template = """
    INSERT INTO 
    user_sessions (training_unit_id, user_id, qualification_id, type, is_done)
    VALUES 
    (?, ?, ?, ?, ?)
    """
    
    insert_values = []
    
    for row in data:
        
        training_unit_id = row[0]
        
        if row[1] != 0:
            for i in range(row[1]):
                insert_values.append((training_unit_id, user_id, qualification_id, "theory", 0))
        
        if row[2] != 0:
            for i in range(row[2]):
                insert_values.append((training_unit_id, user_id, qualification_id, "practical", 0))
        
        if row[3] != 0:
            for i in range(row[3]):
                insert_values.append((training_unit_id, user_id, qualification_id, "additional", 0))

    if insert_values:
        db_cursor = connect()
        db_cursor.executemany(insert_template, insert_values)
        disconnect(db_cursor)
        


def get_qualifications():
    db_cursor = connect()
    #ID, level, titel
    sqlite_query = "SELECT * FROM qualifications"
    db_cursor.execute(sqlite_query)
    
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

def get_qualification_ids():
    db_cursor = connect()
    #ID, level, titel
    sqlite_query = "SELECT (qualification_id) FROM qualifications"
    db_cursor.execute(sqlite_query)
    
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

def get_qualifications_titel(qualification_id):
    db_cursor = connect()
    #ID, level, titel
    sqlite_query = "SELECT titel FROM qualifications WHERE qualification_id = (?)"
    db_cursor.execute(sqlite_query,(qualification_id, ))
    
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record


def get_qualifications_for_user(user_id):
    db_cursor = connect()
    sqlite_query = """
    SELECT
    user_qualifications.qualification_id,
    qualifications.qualification_level, qualifications.titel, qualifications.session_amount, 
    user_qualifications.amount_sessions_completed,
    user_qualifications.is_completed
    FROM
    user_qualifications
    INNER JOIN
    qualifications
    ON
    user_qualifications.qualification_id = qualifications.qualification_id
    WHERE
    user_qualifications.user_id = (?)
    """
    db_cursor.execute(sqlite_query, (user_id, ))
    
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record



#Maybe split in tqo? -> For evry session learngoals/content/comments is sended with it. Do two querys 1. for all sessions 2. for the needed training unit data
def get_training_units_and_sessions(qualification_id, user_id):
    db_cursor = connect()
    sqlite_query = """
    SELECT 
    training_units.training_unit_id, training_units.titel, training_units.number, training_units.learngoals, training_units.content, training_units.comments,
    user_sessions.session_id, user_sessions.type, user_sessions.is_done, user_sessions.is_done_timestamp
    FROM 
    user_sessions
    INNER JOIN 
    training_units
    ON 
    training_units.training_unit_id = user_sessions.training_unit_id
    WHERE 
    user_sessions.qualification_id = (?)
    AND 
    user_sessions.user_id = (?)
    """
    
    db_cursor.execute(sqlite_query, (qualification_id, user_id))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record


def get_session(user_id, session_id):
    db_cursor = connect()
    sqlite_query = """
    SELECT * FROM user_sessions
    WHERE session_id = (?)
    AND user_id = (?)
    """
    
    db_cursor.execute(sqlite_query, (session_id, user_id))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

def set_session_is_done(user_id, session_id, timestamp):
    db_cursor = connect()
    sqlite_query = """
    UPDATE user_sessions
    SET is_done = 1, is_done_timestamp = (?)
    WHERE session_id = (?)
    AND user_id = (?)
    """
    
    db_cursor.execute(sqlite_query, (timestamp, session_id, user_id))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record


def set_session_is_not_done(user_id, session_id):
    db_cursor = connect()
    sqlite_query = """
    UPDATE user_sessions
    SET is_done = 0, is_done_timestamp = (?)
    WHERE session_id = (?)
    AND user_id = (?)
    """
    
    db_cursor.execute(sqlite_query, (NULL, session_id, user_id))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

def check_if_user_has_done_all_sessions(user_id, qualification_id):
    db_cursor = connect()
    sqlite_query = """
    SELECT 
    user_qualifications.amount_sessions_completed, qualifications.session_amount
    FROM
    user_qualifications
    INNER JOIN
    qualifications
    ON
    user_qualifications.qualification_id = qualifications.qualification_id
    WHERE
    user_qualifications.qualification_id = (?)
    AND
    user_qualifications.user_id = (?)
    """
    
    db_cursor.execute(sqlite_query, (qualification_id, user_id))
    data = db_cursor.fetchone()
    disconnect(db_cursor)
    
    print("USERID: ", user_id, "QUAL ID: ", qualification_id)
    
    
    #Id sessions_done >= session_amount
    if(data[0] >= data[1]):
        return True
    else:
        return False

def set_qualification_as_completed(qualification_id, user_id, is_done = 1):
    db_cursor = connect()
    sqlite_query = """
    UPDATE user_qualifications
    SET is_completed = (?)
    WHERE qualification_id = (?)
    AND user_id = (?)
    """
    
    db_cursor.execute(sqlite_query, (is_done, qualification_id, user_id))
    disconnect(db_cursor)


    


def get_qualification_pdf_table(qualification_id, user_id):
    db_cursor = connect()
    sqlite_query = """
    SELECT
    training_units.number,training_units.titel,
    user_sessions.is_done_timestamp
    FROM
    user_sessions
    INNER JOIN training_units ON training_units.training_unit_id = user_sessions.training_unit_id
    WHERE user_sessions.qualification_id = (?)
    AND
    user_id = (?)
    """
    
    db_cursor.execute(sqlite_query, (qualification_id, user_id))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record




# New Code:

#user_id = int
#qualification_ids = tupel of qualification ids
def add_qualifications_to_user(user_id, qualification_ids):
    script_query = ""
    
    for qualification_id in qualification_ids:
        script_query += f"""
        INSERT INTO 
        user_qualifications
        (user_id, qualification_id, amount_training_units_completed, amount_sessions_completed, is_completed, is_completed_timestamp)
        VALUES 
        ({user_id} ,{qualification_id[0]}, 0, 0, 0, NULL);
        """
    
    db_cursor = connect()
    db_cursor.executescript(script_query)
    disconnect(db_cursor)
    return


#Work
#qualification_id tupel
def get_training_units(qualification_ids):
    
    
    db_cursor = connect()
    record = []
    for qualification_id in qualification_ids:
        query = """
        SELECT 
        training_unit_id
        FROM
        qualifications_training_units
        WHERE 
        qualifications_training_units.qualification_id = (?)
        """
        db_cursor.execute(query, (qualification_id[0], ))
        record += db_cursor.fetchall()
        
    disconnect(db_cursor)
    return record


#training_units tupel
def add_training_units_users(training_units, user_id):
    script_query = ""

    for training_unit in training_units:
        script_query += f"""
        INSERT INTO
        training_units_users
        (training_unit_id, user_id, amount_sessions_done, is_completed, is_completed_timestamp)
        VALUES
        ({training_unit[0]}, {user_id}, 0, 0, NULL);
        """
    db_cursor = connect()
    db_cursor.executescript(script_query)
    disconnect(db_cursor)
    return


def add_all_user_sessions(user_id):
    
    #Get amount of sessions of each training unit
    
    db_cursor = connect()
    
    query = """
    SELECT
    training_units_users.training_unit_id, 
    qualifications_training_units.qualification_id, 
    training_units.practical_sessions, 
    training_units.theory_sessions, 
    training_units.additional_sessions
    FROM
    training_units_users
    INNER JOIN
    training_units
    ON
    training_units_users.training_unit_id = training_units.training_unit_id
    INNER JOIN
    qualifications_training_units
    ON
    qualifications_training_units.training_unit_id = training_units_users.training_unit_id
    WHERE
    training_units_users.user_id = (?)
    """
    db_cursor.execute(query, (user_id, ))
    training_units_data = db_cursor.fetchall()
    
    script_query = ""
    
    #for each training unit add sessions
    #-> Monitor memory usage because of huge query strings
    for training_unit in training_units_data:
        
        amount_practical_sessions = training_unit[2]
        amount_theory_sessions = training_unit[3]
        amount_additional_sessions = training_unit[4]
        
        #theory sessions
        for x in range(amount_theory_sessions):
            script_query += f"""
            INSERT INTO
            user_sessions
            (training_unit_id, qualification_id, user_id, type, is_done, is_done_timestamp)
            VALUES
            ({training_unit[0]}, {training_unit[1]}, {user_id}, "theory", 0, NULL);
            """
        
        #practical sessions:
        for x in range(amount_practical_sessions):
            script_query += f"""
            INSERT INTO
            user_sessions
            (training_unit_id, qualification_id, user_id, type, is_done, is_done_timestamp)
            VALUES
            ({training_unit[0]}, {training_unit[1]}, {user_id}, "practical", 0, NULL);
            """
        
        #additonal sessions
        for x in range(amount_additional_sessions):
            script_query += f"""
            INSERT INTO
            user_sessions
            (training_unit_id, qualification_id, user_id, type, is_done, is_done_timestamp)
            VALUES
            ({training_unit[0]}, {training_unit[1]}, {user_id}, "additional", 0, NULL);
            """
            
    print("Add sessions string query in bytes: ", len(script_query.encode('utf-8')))
    db_cursor.executescript(script_query)
    disconnect(db_cursor)
    return
    


def check_if_QRCode_already_exist(code):
    
    query = """
    SELECT
    code
    FROM 
    certificates
    WHERE
    code = (?)
    """
    
    db_cursor = connect()
    db_cursor.execute(query, (code,))
    record = db_cursor.fetchall()
    
    if len(record) > 0:
        return True
    else:
        return False
    
    
def add_QRCode_qualification_certificate(qualification_id, creator_user_id, end_timestamp, max_amount_of_uses):
    query = """
    INSERT INTO 
    certificates
    (qualification_id, created_by_user_id, created_at_timestamp, end_timestamp, amount_of_uses, max_amount_of_uses)
    VALUES
    (?,?, datetime(current_timestamp, 'localtime'),?, ?, ?)
    """ 
    
    db_cursor = connect()
    db_cursor.execute(query, (qualification_id, creator_user_id, end_timestamp, 0, max_amount_of_uses))
    last_id = db_cursor.lastrowid
    disconnect(db_cursor)
    return last_id



def set_qrCode_qualification_certificate_code(certificate_id, code):
    query = """
    UPDATE
    certificates
    SET
    code = (?)
    WHERE
    certificates.certificate_id = (?) 
    """ 
    
    db_cursor = connect()
    db_cursor.execute(query, (code, certificate_id))
    disconnect(db_cursor)
    return

def find_qualification_certificate(qr_code):
    query = """
    SELECT
    *
    FROM
    certificates
    WHERE
    certificates.code = (?)
    """ 
    
    db_cursor = connect()
    db_cursor.execute(query, (qr_code,))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

#Increase or decrease amount of useses on qualification certificate
def increase_amount_uses_of_qualification_certificate(certificate_id, amount = 1):
    query = """
    UPDATE
    certificates
    SET
    amount_of_uses = amount_of_uses + ?
    WHERE
    certificate_id = ?
    """ 
    db_cursor = connect()
    db_cursor.execute(query, (amount, certificate_id))
    disconnect(db_cursor)
    return


def check_if_user_has_qualification(user_id, qualification_id):
    query = """
    SELECT
    user_qualifications.is_completed
    FROM
    user_qualifications
    WHERE
    user_qualifications.qualification_id = ?
    AND
    user_qualifications.user_id = ?
    """
    
    db_cursor = connect()
    db_cursor.execute(query, (qualification_id, user_id))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    
    if record[0][0] == 1:
        return True
    else:
        return False


def get_created_qualification_certificate_from_user(user_id):
    query = """
    SELECT
    *
    FROM
    certificates
    WHERE
    certificates.created_by_user_id = (?)
    """ 

    db_cursor = connect()
    db_cursor.execute(query, (user_id,))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

def get_user_data_by_id(user_id):
    query = """
    SELECT
    *
    FROM
    users
    WHERE
    users.user_id = (?)
    """ 

    db_cursor = connect()
    db_cursor.execute(query, (user_id,))
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

def delete_qualification_certificate(certificate_id, user_id):
    query = """
    DELETE
    FROM
    certificates
    WHERE
    certificates.created_by_user_id = (?)
    AND
    certificates.certificate_id = (?)
    """ 
    db_cursor = connect()
    db_cursor.execute(query, (user_id, certificate_id))
    disconnect(db_cursor)
    return


def get_settings_for_certificate_creation():
    query = """
    SELECT
    system_settings.certificate_max_amount,
    system_settings.certificate_life_time
    FROM
    system_settings
    """ 

    db_cursor = connect()
    db_cursor.execute(query)
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

def get_setting_certificate_life_time():
    query = """
    SELECT
    system_settings.certificate_life_time
    FROM
    system_settings
    """ 

    db_cursor = connect()
    db_cursor.execute(query)
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record

def get_setting_certificate_max_amount_per_teacher():
    query = """
    SELECT
    system_settings.certificate_max_amount
    FROM
    system_settings
    """ 

    db_cursor = connect()
    db_cursor.execute(query)
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record


def get_setting_cron_certificate_cleanup_interval():
    query = """
    SELECT
    system_settings.cron_certificate_cleanup_interval
    FROM
    system_settings
    """ 

    db_cursor = connect()
    db_cursor.execute(query)
    record = db_cursor.fetchall()
    disconnect(db_cursor)
    return record


def update_certificate(qualification_id, max_amount_of_uses, certificate_id, user_id):
    query = """
    UPDATE
    certificates
    SET
    qualification_id = (?),
    max_amount_of_uses = (?)
    WHERE
    certificates.certificate_id = (?)
    AND
    certificates.created_by_user_id = (?)
    """ 
    db_cursor = connect()
    db_cursor.execute(query, (qualification_id, max_amount_of_uses, certificate_id, user_id))
    disconnect(db_cursor)
    return