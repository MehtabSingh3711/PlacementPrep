# Frontend Design Document

## JavaFX Desktop Interface for Context-Aware Conversational Chatbot

**Document Version:** 1.0  
**Date:** January 21, 2026  
**Author:** Senior UI/UX Designer & Frontend Software Architect  
**Status:** Final – Implementation Ready  

---

## 1. Introduction

This document defines the frontend design specifications for a Java-based desktop chat application built using JavaFX. The application serves as the user interface for a Context-Aware General Conversational Chatbot, interacting with a Python backend via REST APIs.

The design emphasizes minimalism, clarity, and professionalism, ensuring high usability in academic and demonstration environments while remaining technically feasible within JavaFX constraints.

---

## 2. Design Goals and Principles

### 2.1 Design Goals
- Provide a clean and intuitive chat interface for general conversations
- Visually differentiate user and chatbot messages
- Ensure readability and accessibility across devices
- Maintain responsiveness during backend API calls
- Demonstrate modern UI principles within JavaFX limitations

### 2.2 Design Principles
- **Simplicity:** Avoid visual clutter and unnecessary UI elements
- **Consistency:** Uniform spacing, typography, and color usage
- **Clarity:** Clear visual feedback for all user actions
- **Responsiveness:** Non-blocking UI interactions
- **Explainability:** UI behavior easily understood during academic evaluation

---

## 3. Visual Theme and Style

### 3.1 Overall Theme
- Minimal, modern, and professional
- Suitable for academic and technical audiences

### 3.2 Color Palette

| Usage | Color | Description |
|----|----|----|
| Primary | Soft Green (#4CAF50) | Primary accent for buttons and highlights |
| Secondary | Light Mint (#A5D6A7) | Message bubble accents |
| Background | Frosted White (#F8FAF9) | Main application background |
| Borders | Light Gray (#E0E0E0) | Subtle separation lines |
| Text (Primary) | Dark Gray (#2E2E2E) | Main text color |
| Text (Secondary) | Medium Gray (#6B6B6B) | Timestamps and metadata |

### 3.3 Glassmorphism Approximation (JavaFX)

Due to JavaFX limitations, glassmorphism is approximated using:
- Semi-transparent backgrounds (`rgba(255,255,255,0.75)`)
- Subtle drop shadows
- Light borders
- Background blur simulated via layered opacity (no true blur)

---

## 4. Typography

### 4.1 Font Family
- **Primary Font:** System default (San Francisco / Segoe UI / Roboto fallback)
- Ensures cross-platform compatibility

### 4.2 Font Sizes

| Element | Size |
|------|----|
| Application Title | 18–20 px |
| Chat Messages | 14–15 px |
| Input Field | 14 px |
| Metadata / Timestamps | 11–12 px |

### 4.3 Font Styling
- Normal weight for messages
- Medium weight for headers
- No italics except placeholders

---

## 5. Layout Structure

### 5.1 High-Level Layout

The application uses a `BorderPane` as the root container:

BorderPane
├── Top: Header Section
├── Center: Chat Display Area
└── Bottom: Input Section


### 5.2 Header Section
- Implemented using `HBox`
- Displays:
  - Application title (left-aligned)
  - Session/User identifier (right-aligned)
- Fixed height with subtle bottom border

### 5.3 Chat Display Area
- Implemented using `ScrollPane` containing a `VBox`
- Features:
  - Vertical stacking of message bubbles
  - Auto-scroll to latest message
  - Padding for readability

### 5.4 Input Section
- Implemented using `HBox`
- Contains:
  - Text input field (expands horizontally)
  - Send button (fixed width)
- Fixed position at bottom

---

## 6. Component Hierarchy

ChatWindow (Stage)
└── Scene
└── BorderPane
├── Header (HBox)
│ ├── Title Label
│ └── Session ID Label
├── ChatArea (ScrollPane)
│ └── MessagesContainer (VBox)
│ ├── MessageBubble (User)
│ ├── MessageBubble (Bot)
│ └── ...
└── InputArea (HBox)
├── TextField (User Input)
└── Button (Send)


---

## 7. Message Bubble Design

### 7.1 User Message Bubble
- Right-aligned
- Background: Light green tint
- Rounded corners (12–16 px radius)
- White text or dark text depending on contrast
- Slight shadow for elevation

### 7.2 Bot Message Bubble
- Left-aligned
- Background: Frosted white with green border
- Rounded corners
- Subtle border accent
- Clear distinction from user messages

### 7.3 Message Metadata
- Optional timestamp below message
- Smaller font size
- Muted color

---

## 8. Interaction Design

### 8.1 Message Sending
- User presses **Enter** or clicks **Send**
- Input field disabled during API call
- Loading indicator displayed

### 8.2 Loading / Typing Indicator
- Small animated dots or spinner
- Displayed within chat area
- Removed once response arrives

### 8.3 Auto-Scroll Behavior
- Chat area automatically scrolls to bottom on:
  - New user message
  - New bot response

---

## 9. UI States

### 9.1 Idle State
- Input enabled
- No loading indicators

### 9.2 Loading State
- Input disabled
- Typing indicator visible
- Send button disabled

### 9.3 Error State
- Error message displayed in chat area or status banner
- Input re-enabled
- Clear, non-technical error text

---

## 10. Error and Edge-Case Handling

### 10.1 Network Errors
- Display user-friendly message:
  “Unable to connect. Please check your network.”

### 10.2 API Errors
- Display generic error message
- Avoid exposing backend or API details

### 10.3 Empty Input
- Prevent submission
- Optional inline warning

### 10.4 Long Messages
- Text wraps automatically
- Scroll enabled within message bubble if necessary

---

## 11. JavaFX-Specific Considerations

### 11.1 Non-Blocking Design
- Backend calls executed using:
  - `Task`
  - `Service`
  - `ExecutorService`
- UI thread never blocked

### 11.2 Styling
- All styles implemented using JavaFX CSS
- No JavaScript or web technologies
- CSS organized into reusable classes

### 11.3 Limitations and Workarounds

| Limitation | Mitigation |
|----|----|
| No native blur | Use opacity and shadows |
| Limited animation | Use subtle transitions |
| Desktop-only | Acceptable for scope |

---

## 12. Accessibility and Usability

- High contrast text/background combinations
- Readable font sizes
- Clear focus states for input fields
- Keyboard-only interaction supported
- Logical tab navigation order

---

## 13. Conclusion

This frontend design provides a modern, clean, and academically appropriate JavaFX-based user interface for a context-aware conversational chatbot. The design balances visual appeal with technical feasibility, ensuring ease of implementation, clarity during demonstrations, and strong alignment with educational evaluation criteria.

---

**End of Document**
