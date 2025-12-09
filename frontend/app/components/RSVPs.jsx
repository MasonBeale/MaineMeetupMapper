import React from 'react';
import PropTypes from 'prop-types';
import styles from "../page.module.css";

// Basic functional component
function RSVPs({ value }) {
  return (
    <div className={styles.integer_display}>
      <h2>Event Name</h2>
      <p className={styles.integer_value}>{value}</p>
      <p className="integer-description">This is an integer: {value}</p>
    </div>
  );
}

RSVPs.propTypes = {
  value: PropTypes.number.isRequired,
};

export default RSVPs;