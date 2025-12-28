import React from 'react';
import clsx from 'clsx';
import styles from './LabExercise.module.css';

// Define the props type for the LabExercise component
type LabExerciseProps = {
  title: string;
  children: React.ReactNode;
};

// Lab Exercise component for book-wide use
export default function LabExercise({ title, children }: LabExerciseProps): JSX.Element {
  return (
    <div className={clsx('lab-exercise', styles.labExerciseContainer)}>
      <div className={clsx('lab-title', styles.labTitle)}>
        <span className={styles.labIcon}>🧪</span>
        <h3 className={styles.labTitleText}>{title}</h3>
      </div>
      <div className={styles.labContent}>
        {children}
      </div>
    </div>
  );
}