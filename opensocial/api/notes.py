from datetime import datetime
from peewee import *
from opensocial.model import BaseModel
from opensocial.api.accounts import Accounts
from opensocial.utilities import UtilitiesAPI

import secrets


class Notes(BaseModel):
    id = IntegerField(primary_key=True)
    creation_date = DateTimeField(default=datetime.utcnow())
    content = TextField()
    creator = ForeignKeyField(Accounts, backref='notes')
    note_id = CharField(50)
    is_edited = BooleanField(default=False)

    def getJSON(self, advanced=False):
        json_object = {
            'note_id': self.note_id,
            'is_edited': self.is_edited,
            'create_date': self.creation_date,
            'creator': self.creator.getJSON()
        }

        if advanced:
            json_object['content'] = self.content

        return json_object

    def newNote(access_token, content):
        newNoteErrors = [
            "invalid_token",
            "short_conten"
        ]

        if Accounts.isValidAccessToken(access_token):
            if len(content) >= 1:
                new_note_id = secrets.token_hex(25)

                Notes.create(creator=Accounts.get(Accounts.access_token == access_token), content=content, note_id=new_note_id)

                return {
                    'status': True,
                    'data': {
                        'note_id': new_note_id
                    }
                }
            else:
                return UtilitiesAPI.errorJson(newNoteErrors[1])
        else:
            return UtilitiesAPI.errorJson(newNoteErrors[0])

    def getNote(access_token, note_id):
        getNoteErrors = [
            "invalid_token",
            "note_not_found"
        ]

        if Accounts.isValidAccessToken(access_token):
            target_note = Notes.get_or_none(
                Notes.note_id == note_id, 
                Notes.creator == Accounts.get(Accounts.access_token == access_token)
            )

            if target_note != None:
                return {
                    'status': True,
                    'data': target_note.getJSON(advanced=True)
                }
            else:
                return UtilitiesAPI.errorJson(getNoteErrors[1])
        else:
            return UtilitiesAPI.errorJson(getNoteErrors[0])

    def getNotes(access_token):
        getNotesErrors = [
            "invalid_token"
        ]

        if Accounts.isValidAccessToken(access_token):
            user_notes = Accounts.get(Accounts.access_token == access_token).notes

            notes_array = []

            for note in user_notes:
                notes_array.append(note.getJSON())

            return {
                'status': True,
                'data': notes_array
            }
        else:
            return UtilitiesAPI.errorJson(getNotesErrors[0])

    
    def editNote(access_token, note_id, content):
        editNoteErrors = [
            "invalid_token",
            "note_not_found",
            "short_content"
        ]

        if Accounts.isValidAccessToken(access_token):
            target_note = Notes.get_or_none(
                Notes.note_id == note_id, 
                Notes.creator == Accounts.get(Accounts.access_token == access_token)
            )

            if target_note != None:
                if len(content) >= 1:
                    target_note.content = content
                    target_note.is_edited = True

                    target_note.save()

                    return {
                        'status': True
                    }
                else:
                    return UtilitiesAPI.errorJson(editNoteErrors[2])
            else:
                return UtilitiesAPI.errorJson(editNoteErrors[1])
        else:
            return UtilitiesAPI.errorJson(editNoteErrors[0])
    
    def deleteNote(access_token, note_id):
        deleteNoteErrors = [
            "invalid_token",
            "note_not_found"
        ]

        if Accounts.isValidAccessToken(access_token):
            target_note = Notes.get_or_none(
                Notes.note_id == note_id, 
                Notes.creator == Accounts.get(Accounts.access_token == access_token)
            )

            if target_note != None:
                target_note.delete_instance()

                return {
                    'status': True
                }
            else:
                return UtilitiesAPI.errorJson(deleteNoteErrors[1])
        else:
            return UtilitiesAPI.errorJson(deleteNoteErrors[0])