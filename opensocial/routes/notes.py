from flask import Blueprint, request
from opensocial.api.notes import Notes


NotesRAPI = Blueprint('Notes', __name__, url_prefix='/notes')


@NotesRAPI.post('/newNote')
def NotesAddAPI():
    params = request.json
    return Notes.newNote(params['access_token'], params['content'])


@NotesRAPI.post('/getNotes')
def NotesGetAPI():
    params = request.json
    return Notes.getNotes(params['access_token'])


@NotesRAPI.post('/getNote')
def NoteGetAPI():
    params = request.json
    return Notes.getNote(params['access_token'], params['note_id'])


@NotesRAPI.post('/editNote')
def NotesEditAPI():
    params = request.json
    return Notes.editNote(params['access_token'], params['note_id'], params['content'])


@NotesRAPI.post('/removeNote')
@NotesRAPI.post('/deleteNote')
def NoteDeleteAPI():
    params = request.json
    return Notes.deleteNote(params['access_token'], params['note_id'])