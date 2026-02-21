import React, { useState, useEffect } from 'react'
import './index.css'

interface Quest {
  id: string;
  title: string;
  description: string;
  xp: number;
  completed: boolean;
}

function App() {
  const [quests, setQuests] = useState<Quest[]>(() => {
    const saved = localStorage.getItem('pixel-quests');
    return saved ? JSON.parse(saved) : [
      { id: '1', title: 'Start Your Journey', description: 'Complete your first task to earn XP!', xp: 50, completed: false },
      { id: '2', title: 'Daily Grind', description: 'Log in and check your quests.', xp: 20, completed: true },
    ];
  });
  const [xp, setXp] = useState(() => {
    const saved = localStorage.getItem('pixel-xp');
    return saved ? parseInt(saved) : 70;
  });
  const [level, setLevel] = useState(1);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newQuest, setNewQuest] = useState({ title: '', description: '', xp: 50 });

  useEffect(() => {
    localStorage.setItem('pixel-quests', JSON.stringify(quests));
  }, [quests]);

  useEffect(() => {
    localStorage.setItem('pixel-xp', xp.toString());
  }, [xp]);

  const toggleQuest = (id: string) => {
    setQuests(quests.map(q => {
      if (q.id === id) {
        const newStatus = !q.completed;
        if (newStatus) setXp(prev => prev + q.xp);
        else setXp(prev => Math.max(0, prev - q.xp));
        return { ...q, completed: newStatus };
      }
      return q;
    }));
  };

  const addQuest = (e: React.FormEvent) => {
    e.preventDefault();
    const quest: Quest = {
      id: Date.now().toString(),
      title: newQuest.title,
      description: newQuest.description,
      xp: newQuest.xp,
      completed: false
    };
    setQuests([...quests, quest]);
    setShowAddModal(false);
    setNewQuest({ title: '', description: '', xp: 50 });
  };

  useEffect(() => {
    const newLevel = Math.floor(xp / 100) + 1;
    if (newLevel !== level) {
      setLevel(newLevel);
    }
  }, [xp, level]);

  const levelProgress = (xp % 100);

  return (
    <div className="container">
      <header className="glass-panel">
        <h1>Pixel Quest</h1>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span className="retro-text" style={{ fontSize: '0.8rem' }}>Hero Progress</span>
            <div className="xp-bar" style={{ width: '300px' }}>
              <div className="xp-fill" style={{ width: `${levelProgress}%` }}></div>
            </div>
          </div>
          <div className="level-badge">LVL {level}</div>
        </div>
        <p className="retro-text" style={{ fontSize: '0.6rem', marginTop: '0.5rem', color: 'var(--accent-color)' }}>
          {xp} XP TOTAL
        </p>
      </header>

      <main>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h2 className="retro-text" style={{ fontSize: '1rem' }}>Active Quests</h2>
          <button onClick={() => setShowAddModal(true)}>+ NEW QUEST</button>
        </div>

        {showAddModal && (
          <div className="glass-panel" style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', zIndex: 100, width: '90%', maxWidth: '400px' }}>
            <h3 className="retro-text" style={{ fontSize: '0.8rem', marginBottom: '1rem' }}>New Quest</h3>
            <form onSubmit={addQuest}>
              <div style={{ marginBottom: '1rem' }}>
                <label className="retro-text" style={{ fontSize: '0.6rem', display: 'block', marginBottom: '0.3rem' }}>Quest Title</label>
                <input
                  type="text"
                  value={newQuest.title}
                  onChange={e => setNewQuest({ ...newQuest, title: e.target.value })}
                  required
                  style={{ width: '100%', padding: '0.5rem', background: 'var(--glass)', border: '1px solid var(--primary-color)', color: 'white' }}
                />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label className="retro-text" style={{ fontSize: '0.6rem', display: 'block', marginBottom: '0.3rem' }}>Description</label>
                <textarea
                  value={newQuest.description}
                  onChange={e => setNewQuest({ ...newQuest, description: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', background: 'var(--glass)', border: '1px solid var(--primary-color)', color: 'white' }}
                />
              </div>
              <div style={{ display: 'flex', gap: '1rem' }}>
                <button type="submit">START QUEST</button>
                <button type="button" onClick={() => setShowAddModal(false)} style={{ background: 'var(--danger-color)' }}>CANCEL</button>
              </div>
            </form>
          </div>
        )}

        {quests.map(quest => (
          <div key={quest.id} className={`glass-panel quest-card ${quest.completed ? 'completed' : ''}`}>
            <div className="quest-info">
              <h3>{quest.title}</h3>
              <p>{quest.description}</p>
              <div style={{ marginTop: '0.5rem' }}>
                <span className="level-badge" style={{ background: 'var(--primary-color)', color: 'white' }}>
                  +{quest.xp} XP
                </span>
              </div>
            </div>
            <button
              onClick={() => toggleQuest(quest.id)}
              style={{ background: quest.completed ? 'var(--success-color)' : 'var(--primary-color)' }}
            >
              {quest.completed ? 'DONE' : 'COMPLETE'}
            </button>
          </div>
        ))}
      </main>

      <footer style={{ marginTop: '3rem', textAlign: 'center', opacity: 0.5 }}>
        <p className="retro-text" style={{ fontSize: '0.5rem' }}>Powered by AntiGravity & Gemini Pro</p>
      </footer>
    </div>
  );
}

export default App
