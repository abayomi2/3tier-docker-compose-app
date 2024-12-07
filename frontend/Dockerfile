# Use a Node.js image for React app
FROM node:16

# Set the working directory
WORKDIR /usr/src/app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy the source code, including the src directory
COPY . .

# Expose port 3000 for the React app
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
