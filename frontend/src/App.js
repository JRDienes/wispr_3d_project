import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Scene from './components/Sphere3D';
import Timeline from './components/Timeline';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
    const [events, setEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [texture, setTexture] = useState(null);

    useEffect(() => {
        // Fetch events from the API
        const fetchEvents = async () => {
            try {
                const response = await axios.get(`${API_URL}/events`);
                setEvents(response.data);
                if (response.data.length > 0) {
                    setSelectedEvent(response.data[0]);
                }
            } catch (error) {
                console.error('Error fetching events:', error);
            }
        };

        fetchEvents();
    }, []);

    useEffect(() => {
        // Load texture when event is selected
        if (selectedEvent) {
            const loadTexture = async () => {
                try {
                    const response = await axios.get(`${API_URL}/event/${selectedEvent.id}/data`, {
                        responseType: 'arraybuffer'
                    });
                    // Process the data and create texture
                    // This is a placeholder - you'll need to implement the actual texture creation
                    setTexture(response.data);
                } catch (error) {
                    console.error('Error loading event data:', error);
                }
            };

            loadTexture();
        }
    }, [selectedEvent]);

    return (
        <div className="app">
            <div className="visualization">
                {selectedEvent && texture && (
                    <Scene data={selectedEvent} texture={texture} />
                )}
            </div>
            <Timeline
                events={events}
                selectedEvent={selectedEvent}
                onEventSelect={setSelectedEvent}
            />
        </div>
    );
}

export default App; 