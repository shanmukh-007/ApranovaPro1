'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Student {
  id: number;
  name: string;
  email: string;
  track: string;
}

export default function CreateSessionPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [students, setStudents] = useState<Student[]>([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    session_type: 'ONE_ON_ONE',
    scheduled_at: '',
    duration_minutes: 60,
    student_ids: [] as number[],
    agenda: '',
    meet_link: '',
    create_meet_link: false
  });

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`${API_URL}/api/students/available/`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStudents(response.data);
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.post(
        `${API_URL}/api/sessions/`,
        formData,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      alert('Session created successfully!');
      router.push('/trainer/sessions');
    } catch (error: any) {
      console.error('Error creating session:', error);
      alert(error.response?.data?.error || 'Failed to create session');
    } finally {
      setLoading(false);
    }
  };

  const handleStudentToggle = (studentId: number) => {
    setFormData(prev => ({
      ...prev,
      student_ids: prev.student_ids.includes(studentId)
        ? prev.student_ids.filter(id => id !== studentId)
        : [...prev.student_ids, studentId]
    }));
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <div className="mb-8">
        <button
          onClick={() => router.back()}
          className="text-purple-600 hover:text-purple-700 mb-4"
        >
          ← Back to Sessions
        </button>
        <h1 className="text-3xl font-bold text-gray-900">Schedule New Session</h1>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 space-y-6">
        {/* Title */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Session Title *
          </label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            placeholder="e.g., Python Basics - Week 1"
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            rows={3}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            placeholder="Brief description of the session..."
          />
        </div>

        {/* Session Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Session Type *
          </label>
          <select
            value={formData.session_type}
            onChange={(e) => setFormData({ ...formData, session_type: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
          >
            <option value="ONE_ON_ONE">One-on-One</option>
            <option value="GROUP">Group Session</option>
            <option value="WORKSHOP">Workshop</option>
          </select>
        </div>

        {/* Date and Time */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Date & Time *
            </label>
            <input
              type="datetime-local"
              required
              value={formData.scheduled_at}
              onChange={(e) => setFormData({ ...formData, scheduled_at: e.target.value })}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Duration (minutes) *
            </label>
            <input
              type="number"
              required
              min="15"
              step="15"
              value={formData.duration_minutes}
              onChange={(e) => setFormData({ ...formData, duration_minutes: parseInt(e.target.value) })}
              className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            />
          </div>
        </div>

        {/* Agenda */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Agenda
          </label>
          <textarea
            value={formData.agenda}
            onChange={(e) => setFormData({ ...formData, agenda: e.target.value })}
            rows={4}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            placeholder="Session agenda and topics to cover..."
          />
        </div>

        {/* Students */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Students *
          </label>
          <div className="border rounded-lg p-4 max-h-64 overflow-y-auto space-y-2">
            {students.length === 0 ? (
              <p className="text-gray-500 text-sm">No enrolled students found</p>
            ) : (
              students.map((student) => (
                <label
                  key={student.id}
                  className="flex items-center gap-3 p-2 hover:bg-gray-50 rounded cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={formData.student_ids.includes(student.id)}
                    onChange={() => handleStudentToggle(student.id)}
                    className="w-4 h-4 text-purple-600 rounded focus:ring-purple-500"
                  />
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{student.name}</div>
                    <div className="text-sm text-gray-500">{student.email} • {student.track}</div>
                  </div>
                </label>
              ))
            )}
          </div>
          <p className="text-sm text-gray-500 mt-2">
            {formData.student_ids.length} student(s) selected
          </p>
        </div>

        {/* Google Meet Link */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Google Meet Link
          </label>
          <input
            type="url"
            value={formData.meet_link}
            onChange={(e) => setFormData({ ...formData, meet_link: e.target.value })}
            className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-600 focus:border-transparent"
            placeholder="https://meet.google.com/xxx-xxxx-xxx"
          />
          <p className="text-sm text-gray-500 mt-2">
            💡 Tip: Create a meeting at <a href="https://meet.google.com/new" target="_blank" rel="noopener noreferrer" className="text-purple-600 hover:underline">meet.google.com/new</a> and paste the link here
          </p>
        </div>

        {/* Submit */}
        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            disabled={loading || formData.student_ids.length === 0}
            className="flex-1 bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold"
          >
            {loading ? 'Creating...' : 'Create Session'}
          </button>
          <button
            type="button"
            onClick={() => router.back()}
            className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
