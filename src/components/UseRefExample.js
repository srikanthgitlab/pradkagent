import React, { useRef, useEffect, useState } from 'react';

function UseRefExample() {
  // Create a ref for the input element
  const inputRef = useRef(null);
  // Create a ref to store the previous value of the input
  const previousValueRef = useRef('');
  const [inputValue, setInputValue] = useState('');

  // UseEffect to update the previous value after the component renders
  useEffect(() => {
    previousValueRef.current = inputValue;
  }, [inputValue]);

  // Function to focus on the input element
  const focusInput = () => {
    inputRef.current.focus();
  };

  const handleChange = (event) => {
    setInputValue(event.target.value);
  };

  return (
    <div>
      {/* Input element with the ref attached */}
      <input
        type="text"
        ref={inputRef}
        value={inputValue}
        onChange={handleChange}
      />
      {/* Button to focus on the input */}
      <button onClick={focusInput}>Focus Input</button>
      {/* Display the current and previous values */}
      <p>Current Value: {inputValue}</p>
      <p>Previous Value: {previousValueRef.current}</p>
    </div>
  );
}

export default UseRefExample;