import React from 'react';
import './Timeline.css';

const Timeline = ({ events, selectedEvent, onEventSelect }) => {
    return (
        <div className="timeline">
            <h2>WISPR Events</h2>
            <div className="timeline-events">
                {events.map((event) => (
                    <button
                        key={event.id}
                        className={`timeline-event ${selectedEvent?.id === event.id ? 'selected' : ''}`}
                        onClick={() => onEventSelect(event)}
                    >
                        <div className="event-preview">
                            <img src={event.preview_url} alt={event.description} />
                        </div>
                        <div className="event-info">
                            <h3>{event.timestamp}</h3>
                            <p>{event.description}</p>
                        </div>
                    </button>
                ))}
            </div>
        </div>
    );
};

export default Timeline; 