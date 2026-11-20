import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { createMovie } from '../../services/apiClient';
import './MovieForm.css';

const INITIAL_FORM_DATA = {
  title: '',
  director: '',
  release_year: '',
  genre: '',
};

function MovieForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState(INITIAL_FORM_DATA);
  const [serverErrors, setServerErrors] = useState({});
  const [submitError, setSubmitError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((currentData) => ({
      ...currentData,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setServerErrors({});
    setSubmitError(null);
    setIsSubmitting(true);

    try {
      await createMovie(formData);
      navigate('/');
    } catch (requestError) {
      if (requestError.response?.status === 400) {
        const errorData = requestError.response.data;
        setServerErrors(
          errorData && typeof errorData === 'object' ? errorData : {},
        );
      } else {
        setSubmitError(requestError);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderFieldError = (fieldName) => {
    const messages = serverErrors[fieldName];
    if (!messages) {
      return null;
    }

    const messageList = Array.isArray(messages) ? messages : [messages];

    return (
      <div className="field-error" role="alert">
        {messageList.map((message, index) => (
          <p key={`${fieldName}-${index}`}>{message}</p>
        ))}
      </div>
    );
  };

  return (
    <section className="movie-form-container">
      <h1>Create Movie</h1>
      <p className="form-subtitle">Add a new movie to the catalog.</p>

      {submitError !== null && (
        <div className="form-error" role="alert">
          {submitError.message}
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate>
        <div className="form-field">
          <label htmlFor="title">Title</label>
          <input
            id="title"
            name="title"
            type="text"
            value={formData.title}
            onChange={handleChange}
          />
          {renderFieldError('title')}
        </div>

        <div className="form-field">
          <label htmlFor="director">Director</label>
          <input
            id="director"
            name="director"
            type="text"
            value={formData.director}
            onChange={handleChange}
          />
          {renderFieldError('director')}
        </div>

        <div className="form-field">
          <label htmlFor="release_year">Release Year</label>
          <input
            id="release_year"
            name="release_year"
            type="number"
            value={formData.release_year}
            onChange={handleChange}
          />
          {renderFieldError('release_year')}
        </div>

        <div className="form-field">
          <label htmlFor="genre">Genre</label>
          <input
            id="genre"
            name="genre"
            type="text"
            value={formData.genre}
            onChange={handleChange}
          />
          {renderFieldError('genre')}
        </div>

        <button className="submit-button" type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Creating...' : 'Create Movie'}
        </button>
      </form>
    </section>
  );
}

export default MovieForm;
