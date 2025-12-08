import React from 'react';
import PropTypes from 'prop-types';

// Basic functional component
function Reviews({ value }) {
  return (
    <div className="integer-display">
      <h2>UserName</h2>
      <p className="integer-value">{value}</p>
      <p className="integer-description">This is an integer: {value}</p>
    </div>
  );
}

Reviews.propTypes = {
  value: PropTypes.number.isRequired,
};

export default Reviews;