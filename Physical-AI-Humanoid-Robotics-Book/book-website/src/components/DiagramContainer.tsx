import React from 'react';
import clsx from 'clsx';
import styles from './DiagramContainer.module.css';

// Define the props type for the DiagramContainer component
type DiagramContainerProps = {
  title?: string;
  children: React.ReactNode;
};

// Diagram Container component for book-wide use
export default function DiagramContainer({ title, children }: DiagramContainerProps): JSX.Element {
  return (
    <div className={clsx('diagram-container', styles.diagramContainer)}>
      {title && <h4 className={styles.diagramTitle}>{title}</h4>}
      <div className={styles.diagramContent}>
        {children}
      </div>
    </div>
  );
}