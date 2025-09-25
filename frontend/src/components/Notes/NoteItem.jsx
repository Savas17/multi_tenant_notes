import React from 'react';

const NoteItem = ({ note }) => (
  <div className="note-item">
    <h3>{note.title}</h3>
    <p>{note.content}</p>
  </div>
);

export default NoteItem;
