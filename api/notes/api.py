import sqlite3
import secrets
import time

from click import edit

from api.utilities import UtilitiesAPI


class NotesAPI:
    def addNewNote(access_token, content):
        errors = [
            "incorrect_token"
        ]

        checkTokenResult = UtilitiesAPI.checkToken(access_token)

        if checkTokenResult['validToken']:
            with sqlite3.connect('opensocial.db') as conn:
                cursor = conn.cursor()

                new_note = cursor.execute('INSERT INTO Notes (content,date,note_id,creator) VALUES (?,?,?,?) RETURNING note_id', (content, time.time(), secrets.token_hex(8), checkTokenResult['id'])).fetchone()

                return { "status": True, "data": { "note_id": new_note[0] } }
        else:
            return { "status": False, "why": errors[0] }, 403
    def getNotes(access_token):
        errors = [
            "incorrect_token"
        ]

        checkTokenResult = UtilitiesAPI.checkToken(access_token)

        if checkTokenResult['validToken']:
            with sqlite3.connect('opensocial.db') as conn:
                cursor = conn.cursor()

                notes_query = cursor.execute('SELECT content,date,note_id FROM Notes WHERE creator = (?) ORDER BY date DESC', [checkTokenResult['id']]).fetchall()
                notes_array = []

                for note in notes_query:
                    noteJson = {
                        "date": note[1],
                        "content": note[0],
                        "note_id": note[2]
                    }

                    notes_array.append(noteJson)

                return { "status": True, "data": notes_array }
        else:
            return { "status": False, "why": errors[0] }, 403
    def getNote(access_token, note_id):
        errors = [
            "incorrect_token",
            "note_not_found"
        ]

        checkTokenResult = UtilitiesAPI.checkToken(access_token)

        if checkTokenResult['validToken']:
            with sqlite3.connect('opensocial.db') as conn:
                cursor = conn.cursor()

                note_query = cursor.execute('SELECT content,date,note_id FROM Notes WHERE note_id = (?)', [note_id]).fetchone()

                if note_query != None: 
                    return { "status": True, "data": { "date": note_query[1], "content": note_query[0], "note_id": note_query[2] } }
                else:
                    return { "status": False, "why": errors[1] }, 404
        else:
            return { "status": False, "why": errors[0] }, 403
    def editNote(access_token, note_id, content):
        errors = [
            "incorrect_token",
            "note_not_found"
        ]

        checkTokenResult = UtilitiesAPI.checkToken(access_token)

        if checkTokenResult['validToken']:
            with sqlite3.connect('opensocial.db') as conn:
                cursor = conn.cursor()

                if cursor.execute('SELECT id FROM Notes WHERE note_id = (?)', [note_id]).fetchone() != None:
                    cursor.execute('UPDATE Notes SET content = (?), is_edited = TRUE WHERE note_id = (?) AND creator = (?)', (content, note_id, checkTokenResult['id']))

                    conn.commit()
                    cursor.close()

                    return { "status": True }
                else:
                    return { "status": False, "why": errors[1] }, 404 
        else:
            return { "status": False, "why": errors[0] }, 403
    def deleteNote(access_token, note_id):
        errors = [
            "incorrect_token",
            "note_not_found"
        ]

        checkTokenResult = UtilitiesAPI.checkToken(access_token)

        if checkTokenResult['validToken']:
            with sqlite3.connect('opensocial.db') as conn:
                cursor = conn.cursor()

                if cursor.execute('SELECT id FROM Notes WHERE note_id = (?)', [note_id]).fetchone() != None:
                    cursor.execute('DELETE FROM Notes WHERE note_id = (?)', [note_id])

                    conn.commit()
                    cursor.close()

                    return { "status": True }
                else:
                    return { "status": False, "why": errors[1] }, 404 
        else:
            return { "status": False, "why": errors[0] }, 403