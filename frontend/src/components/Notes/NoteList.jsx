import React from 'react';
import NoteItem from './NoteItem';

const NoteList = ({ notes }) => (
  <div>
    {notes.map(note => (
      <NoteItem key={note.id} note={note} />
    ))}
  </div>
);

export default NoteList;
