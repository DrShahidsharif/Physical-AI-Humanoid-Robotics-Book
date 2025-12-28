import React from 'react';
import clsx from 'clsx';
import styles from './LearningGoals.module.css';

// Define the props type for the LearningGoals component
type LearningGoalsProps = {
  children: React.ReactNode;
};

// Learning Goals component for book-wide use
export default function LearningGoals({ children }: LearningGoalsProps): JSX.Element {
  return (
    <div className={clsx('learning-goals', styles.learningGoalsContainer)}>
      <div className={styles.learningGoalsHeader}>
        <h3>🎯 Learning Goals</h3>
      </div>
      <div className={styles.learningGoalsContent}>
        {children}
      </div>
    </div>
  );
}