import React from 'react'
import styles from './styles.scss'

const GenericStatusLoading = () => (
  <div className={styles.loader__wrapper}>
    <div className={styles.loader}>Loading...</div>
  </div>
)

export default GenericStatusLoading
