from flask import Blueprint, request
from api.notes.api import NotesAPI


NotesRoutesAPI = Blueprint("NotesAPI", __name__, url_prefix='/notes')


@NotesRoutesAPI.post('/newNote')
def NotesAddAPI():
    params = request.json
    return NotesAPI.addNewNote(params['access_token'], params['content'])


@NotesRoutesAPI.post('/getNotes')
def NotesGetAPI():
    params = request.json
    return NotesAPI.getNotes(params['access_token'])


@NotesRoutesAPI.post('/getNote')
def NoteGetAPI():
    params = request.json
    return NotesAPI.getNote(params['access_token'], params['note_id'])


@NotesRoutesAPI.post('/editNote')
def NotesEditAPI():
    params = request.json
    return NotesAPI.editNote(params['access_token'], params['note_id'], params['content'])


@NotesRoutesAPI.post('/deleteNote')
def NoteDeleteAPI():
    params = request.json
    return NotesAPI.deleteNote(params['access_token'], params['note_id'])