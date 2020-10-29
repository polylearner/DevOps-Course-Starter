/// <reference types="Cypress" />

describe('To App', () => {
    it('successfully loads', () => {
        cy.visit('http://127.0.0.1:5000/')
        cy.get('title').should("contain", "To-Do App")
    })
})

describe('To App', () => {
    it('successfully post', () => {
        cy.visit('http://127.0.0.1:5000/')
        cy.get('#title').type('Cypress Test')
        cy.get(':nth-child(2) > :nth-child(1) > .form-inline > .btn').click()
        cy.get('ul').should('contain', 'Cypress Test')
    })
})

describe('To App', () => {
    it('successfully delete', () => {
        cy.visit('http://127.0.0.1:5000/')
        cy.get('ul').should('contain', 'Cypress Test')
            //# cy.get('ul').contains('Cypress Test').get('A#Delete').click()
        cy.get(':nth-child(2) > .list-group > .list-group-item > .row > :nth-child(3) > .form-check > .form-inline > #Delete').click()
    })
})