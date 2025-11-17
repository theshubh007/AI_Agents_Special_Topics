def get_user_choice(prompt: str, options: list = None) -> str:
    """Get user input for confirmation or choice.
    
    Args:
        prompt: The question or prompt to display
        options: Optional list of valid options
    
    Returns:
        User's response as string
    """
    print(f"\n{prompt}")
    
    if options:
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        print()
    
    response = input("Your choice: ").strip()
    return response
