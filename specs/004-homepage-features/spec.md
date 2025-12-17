# Specification: Homepage Features (Chatbot & Translation)

**Feature**: Homepage Features
**Goal**: Add two new visually appealing sections to the homepage highlighting the AI Chatbot and Urdu Translation capabilities.

## 1. Content Requirements

### 1.1. Feature 1: AI Chatbot Integration
- **Headline**: "Your Personal AI Tutor" (or similar).
- **Description**: Highlighting the ability to ask questions, get code help, and interact with the course material dynamically.
- **Visual**: A representation of a chat interface or a robot assistant icon.

### 1.2. Feature 2: Urdu Language Support
- **Headline**: "Learn in Your Language" (Urdu Translation).
- **Description**: Emphasize accessibility and the ability to read the complex Physical AI content in Urdu.
- **Visual**: A symbol representing translation (e.g., 'A' -> 'Urdu char') or a book icon.

## 2. Design Requirements
- **Aesthetic**: Must match the "MindSphere" dark theme (Black background, Green accents).
- **Layout**: Two distinct sections following the Hero.
  - **Option**: Alternating layout (Text-Image / Image-Text) or side-by-side cards.
  - **Decision**: Side-by-side "Glassmorphism" cards to maintain the sleek, modern look.
- **Responsiveness**: Stack vertically on mobile.

## 3. Technical Implementation
- **File**: `src/pages/index.tsx`
  - Add a new `HomepageFeatures` component or distinct sections.
- **File**: `src/css/custom.css`
  - Styles for `.featureSection`, `.featureCard`, `.featureIcon`.

## 4. Acceptance Criteria
- Two new sections exist on the homepage below the hero.
- Section 1 clearly promotes the Chatbot.
- Section 2 clearly promotes Urdu Translation.
- Design is consistent with the dark/green theme.
